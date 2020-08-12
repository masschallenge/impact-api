from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import loader

from rest_framework.response import Response

from accelerator.models import MentorProgramOfficeHour
from ...minimal_email_handler import MinimalEmailHandler
from ...permissions.v1_api_permissions import OfficeHourMentorPermission
from ...v1.views.impact_view import ImpactView
from ...v1.views.utils import (
    get_office_hour_shared_context
)

User = get_user_model()

DEFAULT_TIMEZONE = 'UTC'
SUBJECT = '[Office Hours] Canceled: {date}, {start_time}'

STAFF_NOTIFICATION = ('on behalf of {mentor_name} at {start_time} '
                      '- {end_time} on {date}')
MENTOR_NOTIFICATION = 'at {start_time} - {end_time} on {date}'
OFFICE_HOUR_SESSION_404 = ("The office hour session does not exist.")
SUCCESS_HEADER = 'Canceled office hours'
FAIL_HEADER = 'Office hour session could not be canceled'


def get_ui_notification(context=None, staff=False):
    if staff:
        return STAFF_NOTIFICATION.format(**context)
    return MENTOR_NOTIFICATION.format(**context)


def get_cancelled_by(mentor_name=None, staff=False):
    to_finalist, to_mentor = mentor_name, 'You have'
    if staff:
        to_finalist = to_mentor = 'MassChallenge has'
    return {
        'mentor': to_mentor,
        'finalist': to_finalist,
    }


class CancelOfficeHourSessionView(ImpactView):
    permission_classes = (OfficeHourMentorPermission,)
    view_name = 'cancel_office_hour_session_view'

    def cancel_office_hour_session(self, office_hour, user, message):
        shared_context = get_office_hour_shared_context(office_hour, message)
        self.header = SUCCESS_HEADER
        if user == office_hour.mentor:
            cancelled_by = get_cancelled_by(shared_context['mentor_name'])
            self.handle_notification(office_hour, shared_context, cancelled_by)
            ui_notification = get_ui_notification(shared_context)
            office_hour.delete()
            return ui_notification, True
        else:
            self.handle_notification(
                office_hour, shared_context, get_cancelled_by(staff=True))
            ui_notification = get_ui_notification(shared_context, staff=True)
            office_hour.delete()
            return ui_notification, True

    def post(self, request):
        message = request.data.get('message', None)
        id = request.data.get('id', None)
        try:
            office_hour = MentorProgramOfficeHour.objects.get(pk=id)
        except MentorProgramOfficeHour.DoesNotExist:
            return self.get_response(False, OFFICE_HOUR_SESSION_404)
        self.check_object_permissions(request, office_hour)
        response_detail, success = self.cancel_office_hour_session(
            office_hour, request.user, message)
        return self.get_response(success, response_detail)

    def get_addressee_info(self, office_hour, mentor_name):
        addressee_dict = {
            'mentor': {'hours_with': '',
                       'to_addrs': [office_hour.mentor.email]}
        }
        if office_hour.finalist:
            addressee_dict['mentor']['hours_with'] = ' with {}'.format(
                office_hour.finalist.get_profile().full_name())
            addressee_dict['finalist'] = {
                'hours_with': ' with {}'.format(mentor_name),
                'to_addrs': [office_hour.finalist.email]
            }
        return addressee_dict

    def handle_notification(self, office_hour, context, cancelled_by):
        for addressee in ['mentor', 'finalist']:
            addressee_info = self.get_addressee_info(
                office_hour, context['mentor_name']).get(addressee, None)
            if addressee_info:
                local_context = {
                    'cancelled_by': cancelled_by[addressee],
                    'hours_with': addressee_info['hours_with'],
                    'dashboard_username': addressee_info['to_addrs'][0],
                }
                local_context.update(context)
                self.send_email(local_context, addressee_info['to_addrs'])

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

    def get_response(self, success, detail):
        return Response({
            'success': success,
            'header': self.header if success else FAIL_HEADER,
            'detail': detail
        })
