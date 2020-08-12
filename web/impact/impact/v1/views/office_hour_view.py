from datetime import timedelta
from dateutil.parser import isoparse
from django.conf import settings
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from accelerator.models import MentorProgramOfficeHour

from ...minimal_email_handler import MinimalEmailHandler
from ...permissions.v1_api_permissions import OfficeHourPermission
from ..serializers.office_hours_serializer import OfficeHourSerializer
from .utils import (
    office_hour_time_info,
    datetime_is_in_past,
)

DEFAULT_TIMEZONE = 'UTC'
FAIL_CREATE_HEADER = 'Office hour session could not be created'
FAIL_EDIT_HEADER = 'Office hour session could not be updated'
SUCCESS_DETAIL = "{start_time} - {end_time} on {date}"
NOT_FOUND_HOUR = ("The office hour session you are trying to update "
                  "doesn't exist")
SUCCESS_PAST_DETAIL = ("This office officehour occurs in the past")
SUCCESS_CREATE_HEADER = 'Office hour session(s) created'
SUCCESS_EDIT_HEADER = 'Office hour updated'

SUBJECT = ("[Office Hours] Confirmation of Office Hours on {date} "
           "from {start_time} to {end_time} ")
CREATE_BODY = (
    "Hi {first_name},\n\n"
    "We’re letting you know that a MassChallenge team member "
    "has created office hours on your behalf. You are scheduled "
    "to hold office hours on {date} at the following times:\n\n"
    "Time: {start_time}-{end_time} ({timezone}) / Location: {location}\n\n"
    "A notification email will be sent to you when a finalist "
    "reserves any of your office hours.\n\n"
    "You can also visit "
    "accelerate.masschallenge.org/newofficehours at any time to view"
    " and manage your office hours\n\n"
    "Thank you for volunteering your time to meet with MassChallenge "
    "Finalists! If you have questions, reach out to your community "
    "manager or contact us at any time via "
    "https://masschallenge.org/contact\n\n"
    "- The MassChallenge Team\n"
)
EDIT_BODY = (
    "Hi {first_name},\n\n"
    "We’re letting you know that a MassChallenge team member "
    "has changed office hours on your behalf. You are now scheduled "
    "to hold office hours on {date} at the following times:\n\n"
    "Time: {start_time}-{end_time} ({timezone}) / Location: {location}\n\n"
    "A notification email will be sent to you when a finalist "
    "reserves any of your office hours.\n\n"
    "You can also visit "
    "accelerate.masschallenge.org/newofficehours at any time to view"
    " and manage your office hours\n\n"
    "Thank you for volunteering your time to meet with MassChallenge "
    "Finalists! If you have questions, reach out to your community "
    "manager or contact us at any time via "
    "https://masschallenge.org/contact\n\n"
    "- The MassChallenge Team\n"
)


def handle_fail(errors, edit=False):
    return Response({
        'errors': errors,
        'header': FAIL_EDIT_HEADER if edit else FAIL_CREATE_HEADER,
        'success': False
    })


def get_email_context(office_hour, last_office_hour=None):
    location = office_hour.location
    context = office_hour_time_info(office_hour, last_office_hour)
    context.update({
        'location': location.name if location else '',
        'mentor_email': office_hour.mentor.email,
        'first_name': office_hour.mentor.first_name,
    })
    return context


class OfficeHourViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'patch')
    queryset = MentorProgramOfficeHour.objects.all()
    serializer_class = OfficeHourSerializer
    permission_classes = (OfficeHourPermission,)
    view_name = 'create_edit_office_hours'

    def perform_save(self, request, serializer, save_operation):
        if not serializer.is_valid():
            return handle_fail(serializer.errors, True)
        save_operation(serializer)
        self.office_hour = serializer.instance
        if request.user != self.office_hour.mentor:
            self.handle_send_mail(self.office_hour, edit=True)
        return self.handle_success([serializer.data], True)

    def handle_response(self, request):
        if request.method == 'PATCH':
            try:
                instance = self.get_object()
            except Http404:
                return handle_fail({"errors": NOT_FOUND_HOUR}, edit=True)
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            save_operation = self.perform_update
        return self.perform_save(request, serializer, save_operation)

    def create(self, request, *args, **kwargs):
        data_sets = parse_date_specs(request.data)
        serializers = [self.get_serializer(data=data) for data in data_sets]
        invalid_serializers = [s for s in serializers if not s.is_valid()]
        if invalid_serializers:
            return handle_fail(invalid_serializers[0].errors)
        for serializer in serializers:
            self.perform_create(serializer)
        first_office_hour = serializers[0].instance
        self.office_hour = first_office_hour
        last_office_hour = serializers[-1].instance
        if request.user != first_office_hour.mentor:
            self.handle_send_mail(
                first_office_hour,
                last_office_hour=last_office_hour)

        return self.handle_success(
            [serializer.data for serializer in serializers])

    def update(self, request, *args, **kwargs):
        return self.handle_response(request)

    def handle_send_mail(self, office_hour, edit=False, last_office_hour=None):
        context = get_email_context(office_hour, last_office_hour)
        body = EDIT_BODY if edit else CREATE_BODY
        MinimalEmailHandler(
            to=[office_hour.mentor.email],
            subject=SUBJECT.format(**context),
            body=body.format(**context),
            from_email=settings.NO_REPLY_EMAIL).send()

    def handle_success(self, data, edit=False,):
        return Response({
            'data': data,
            'header': SUCCESS_EDIT_HEADER if edit else SUCCESS_CREATE_HEADER,
            "detail": SUCCESS_PAST_DETAIL if datetime_is_in_past(
                self.office_hour.start_date_time) else "",
            'success': True
        })


def parse_date_specs(data):
    datasets = []
    thirty_minutes = timedelta(minutes=30)
    start_date_time = isoparse(data['start_date_time'])
    end_date_time = isoparse(data['end_date_time'])
    if end_date_time < start_date_time + thirty_minutes:
        return [data]  # let serializer handle this error
    current_session_end = start_date_time + thirty_minutes
    while current_session_end <= end_date_time:
        dataset = data.copy()
        dataset['start_date_time'] = start_date_time
        dataset['end_date_time'] = current_session_end
        datasets.append(dataset)
        start_date_time = current_session_end
        current_session_end += thirty_minutes
    return datasets
