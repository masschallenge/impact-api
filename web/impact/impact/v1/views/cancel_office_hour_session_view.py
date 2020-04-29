from django.contrib.sites.models import Site
from pytz import timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import loader
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from accelerator.models import MentorProgramOfficeHour, Location
from impact.minimal_email_handler import MinimalEmailHandler
from impact.permissions.v1_api_permissions import OfficeHourPermission
from impact.v1.views.impact_view import ImpactView

User = get_user_model()

DEFAULT_TIMEZONE = 'UTC'
SUBJECT = '[Office Hours] Canceled: {date}, {start_time}'

STAFF_NOTIFICATION = 'Canceled office hours on behalf of {} at {} - {} on {}'
MENTOR_NOTIFICATION = 'Canceled office hours at {} - {} on {}'
PERMISSION_DENIED = 'Office hour session could not be canceled. ' \
                    'You do not have permission to cancel that session'


def get_office_hours_list_url(family_slug, program_slug):
    site_url = Site.objects.get_current()
    return 'https://{}/officehours/list/{}/{}'.format(
        site_url, family_slug, program_slug)


def default_timezone(program_family):
    location = Location.objects.filter(
        programfamilylocation__primary=True,
        programfamilylocation__program_family=program_family).exists()
    return location.timezone if location else DEFAULT_TIMEZONE


def get_office_hour_shared_context(office_hour, message=None):
    family_slug = office_hour.program.program_family.url_slug
    program_slug = office_hour.program.url_slug
    tz = timezone(default_timezone(office_hour.program.program_family))
    date = office_hour.start_date_time.astimezone(tz).strftime('%A, %d %B, %Y')
    start_time = office_hour.start_date_time.astimezone(tz).strftime('%I:%M%p')
    end_time = office_hour.end_date_time.astimezone(tz).strftime('%I:%M%p')
    return {
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'location': office_hour.location.name if office_hour.location else '',
        'dashboard_url': get_office_hours_list_url(family_slug, program_slug),
        'mentor_name': office_hour.mentor.get_profile().full_name(),
        'phone': office_hour.program.program_family.phone_number,
        'message': message,
    }


def get_ui_notification(context, staff=False):
    if staff:
        return STAFF_NOTIFICATION.format(
            context['mentor_name'], context['start_time'],
            context['end_time'], context['date'])
    return MENTOR_NOTIFICATION.format(
        context['start_time'], context['end_time'], context['date'])


class CancelOfficeHourSessionView(ImpactView):
    permission_classes = (OfficeHourPermission,)
    view_name = 'cancel_office_hour_session_view'

    def cancel_office_hour_session(self, office_hour, user, message):
        shared_context = get_office_hour_shared_context(office_hour, message)
        if user == office_hour.mentor:
            if office_hour.finalist:
                raise PermissionDenied(PERMISSION_DENIED)
            ui_notification = get_ui_notification(shared_context)
            office_hour.delete()
            return ui_notification
        else:
            self.handle_notification(office_hour, shared_context)
            ui_notification = get_ui_notification(shared_context, staff=True)
            office_hour.delete()
            return ui_notification

    def send_email(self, context, to_addr):
        html_email = loader.render_to_string(
            'emails/cancel_office_hour_session_email.html',
            context
        )
        MinimalEmailHandler(
            to=to_addr,
            subject=SUBJECT.format(**context),
            body=None,
            from_email=settings.NO_REPLY_EMAIL,
            attach_alternative=[html_email, 'text/html'],
        ).send()

    def post(self, request):
        message = request.data.get('message', None)
        id = request.data.get('id', None)
        office_hour = get_object_or_404(MentorProgramOfficeHour, id=id)
        self.check_object_permissions(request, office_hour)
        response_detail = self.cancel_office_hour_session(
            office_hour, request.user, message)
        return Response({'detail': response_detail})

    def get_addressee_info(self, office_hour, mentor_name):
        addressee_dict = {
            'mentor': {'hours_with': '',
                       'to_addrs': [office_hour.mentor.email]}
        }
        if office_hour.finalist:
            addressee_dict['mentor']['hours_with'] = ' with {}'.format(
                office_hour.finalist.get_profile().full_name())
            addressee_dict['finalist'] = {
                'hours_with': f' with {mentor_name}',
                'to_addrs': [office_hour.finalist.email]
            }
        return addressee_dict

    def handle_notification(self, office_hour, context):
        for addressee in ['mentor', 'finalist']:
            addressee_info = self.get_addressee_info(
                office_hour, context['mentor_name']).get(addressee, None)
            if addressee_info:
                local_context = {
                    'cancelled_by': 'MassChallenge has',
                    'hours_with': addressee_info['hours_with'],
                    'dashboard_username': addressee_info['to_addrs'][0],
                }
                local_context.update(context)
                self.send_email(local_context, addressee_info['to_addrs'])
