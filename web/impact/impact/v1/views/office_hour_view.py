from django.conf import settings
from pytz import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from accelerator.models import MentorProgramOfficeHour

from impact.minimal_email_handler import MinimalEmailHandler
from impact.permissions.v1_api_permissions import OfficeHourPermission
from impact.v1.serializers.office_hours import OfficeHourSerializer

FAIL_CREATE_HEADER = 'Office hour session could not be created'
FAIL_EDIT_HEADER = 'Office hour session could not be modified'
SUCCESS_CREATE_HEADER = 'Office hour session created'
SUCCESS_EDIT_HEADER = 'Office hour session modified'

SUBJ = ("[Office Hours] Confirmation of Office Hours on {date}" +
        "from {start_time} to {end_time} ")
CREATE_BODY = (
    "Hi {first_name},\n\n"
    "We’re letting you know that a MassChallenge team member "
    "has created office hours on your behalf. You are scheduled "
    "to hold office hours on {date} at the following times:\n\n"
    "Time: {start_time}-{end_time} Timezone / Location: {location}\n\n"
    "A notification email will be sent to you when a finalist "
    "reserves any of your office hours.\n\n"
    "You can also visit "
    "<a href='https://accelerate.masschallenge.org/officehours'>"
    "accelerate.masschallenge.org/officehours</a> at any time to view"
    " and manage your office hours\n\n"
    "Thank you for volunteering your time to meet with MassChallenge "
    "Finalists! If you have questions, reach out to your community "
    "manager or contact us at any time via "
    "<a href='https://masschallenge.org/contact'>"
    "https://masschallenge.org/contact</a>\n\n"
    "- The MassChallenge Team\n"
)
EDIT_BODY = (
    "Hi {first_name},\n\n"
    "We’re letting you know that a MassChallenge team member "
    "has changed office hours on your behalf. You are now scheduled "
    "to hold office hours on {date} at the following times:\n\n"
    "Time: {start_time}-{end_time} Timezone / Location: {location}\n\n"
    "A notification email will be sent to you when a finalist "
    "reserves any of your office hours.\n\n"
    "You can also visit "
    "<a href='https://accelerate.masschallenge.org/officehours'>"
    "accelerate.masschallenge.org/officehours</a> at any time to view"
    " and manage your office hours\n\n"
    "Thank you for volunteering your time to meet with MassChallenge "
    "Finalists! If you have questions, reach out to your community "
    "manager or contact us at any time via "
    "<a href='https://masschallenge.org/contact'>"
    "https://masschallenge.org/contact</a>\n\n"
    "- The MassChallenge Team\n"
)


def handle_success(data, edit=False):
    return Response({
        'data': data,
        'header': SUCCESS_EDIT_HEADER if edit else SUCCESS_CREATE_HEADER,
        'success': True
    })


def handle_fail(errors, edit=False):
    return Response({
        'errors': errors,
        'header': FAIL_EDIT_HEADER if edit else FAIL_CREATE_HEADER,
        'success': False
    })


def get_email_context(office_hour):
    location = office_hour.location
    tz = timezone(location.timezone if location else 'UTC')
    date = office_hour.start_date_time.astimezone(tz).strftime('%A, %d %B, %Y')
    start_time = office_hour.start_date_time.astimezone(tz).strftime('%I:%M%p')
    end_time = office_hour.end_date_time.astimezone(tz).strftime('%I:%M%p')
    return {
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'location': office_hour.location.name if office_hour.location else '',
        'mentor_email': office_hour.mentor.email,
        'first_name': office_hour.mentor.first_name,
    }


class OfficeHourViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'patch')
    queryset = MentorProgramOfficeHour.objects.all()
    serializer_class = OfficeHourSerializer
    permission_classes = (OfficeHourPermission,)
    view_name = 'create_edit_office_hours'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return handle_fail(serializer.errors)
        self.perform_create(serializer)
        office_hour = serializer.instance
        if request.user != office_hour.mentor:
            self.handle_send_mail(office_hour)
        return handle_success(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=False)
        if not serializer.is_valid():
            return handle_fail(serializer.errors)
        self.perform_update(serializer)
        office_hour = serializer.instance
        if request.user != office_hour.mentor:
            self.handle_send_mail(office_hour, edit=True)
        return handle_success(serializer.data)

    def handle_send_mail(self, office_hour, edit=False):
        context = get_email_context(office_hour)
        body = EDIT_BODY if edit else CREATE_BODY
        MinimalEmailHandler(
            to=[office_hour.mentor.email],
            subject=SUBJ.format(**context),
            body=body.format(**context),
            from_email=settings.NO_REPLY_EMAIL,
        ).send()