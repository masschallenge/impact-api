from django.contrib.auth import get_user_model
from django.template import loader

from rest_framework.response import Response

from ...permissions.v1_api_permissions import OfficeHourFinalistPermission
from .impact_view import ImpactView
from .utils import (
    email_template_path,
    office_hour_time_info,
)
from ...minimal_email_handler import send_email
from accelerator_abstract.models.base_user_utils import is_employee
from mc.utils import swapper_model
MentorProgramOfficeHour = swapper_model("MentorProgramOfficeHour")
User = get_user_model()

mentor_template_name = "cancel_office_hour_reservation_email_to_mentor.html"
finalist_template_name = ("cancel_office_hour_reservation_email_to_finalist."
                          "html")
SUBJECT_LINE = "MassChallenge | Cancelled Office Hours with {} {}"
NO_SUCH_RESERVATION = "That session is not reserved."
NO_SUCH_OFFICE_HOUR = "The specified office hour was not found."
SUCCESS_NOTIFICATION = ("Canceled reservation for {finalist_name} with "
                        "{mentor_name} on {date} at {time}")
SUCCESS_HEADER = 'Canceled office hour reservation'
FAIL_HEADER = 'Office hour reservation could not be canceled'


class CancelOfficeHourReservationView(ImpactView):
    permission_classes = (OfficeHourFinalistPermission, )
    view_name = "cancel_office_hours_reservation"
    posted_fields = ["office_hour_id",
                     "message"]

    def _extract_field(self, data, field):
        setattr(self, field, data.get(field, None))

    def _extract_posted_data(self, data, fields):
        for field in fields:
            self._extract_field(data, field)

    def post(self, request):
        self._extract_posted_data(request.data, self.posted_fields)
        self.user = request.user
        self.office_hour = MentorProgramOfficeHour.objects.filter(
                pk=self.office_hour_id).first()
        can_cancel, detail = self.check_can_cancel()
        if can_cancel:
            self.check_object_permissions(request, self.office_hour)
            self.process_cancellation()
        return Response({
            "success": can_cancel,
            "header": SUCCESS_HEADER if can_cancel else FAIL_HEADER,
            "detail": detail,
        })

    def check_can_cancel(self):
        if self.office_hour is None:
            return False, NO_SUCH_OFFICE_HOUR
        elif self.office_hour.finalist is None:
            return False, NO_SUCH_RESERVATION
        else:
            return True, formatted_success_notification(self.office_hour)

    def process_cancellation(self):
        send_email(**self.prepare_email_notification(self.office_hour.mentor,
                                                     self.office_hour.finalist,
                                                     mentor_template_name))
        send_email(**self.prepare_email_notification(self.office_hour.finalist,
                                                     self.office_hour.mentor,
                                                     finalist_template_name))
        self._cancel_reservation()

    def _cancel_reservation(self):
        self.office_hour.finalist = None
        self.office_hour.save()

    def prepare_email_notification(self,
                                   recipient,
                                   counterpart,
                                   template_name):
        template_path = email_template_path(template_name)
        cancelling_party = self._cancelling_party_name()
        template_context = office_hour_time_info(self.office_hour)
        template_context.update({"recipient": recipient,
                                 "counterpart": counterpart,
                                 "cancelling_party": cancelling_party,
                                 "custom_message": self.message})
        subject = SUBJECT_LINE.format(counterpart.first_name,
                                      counterpart.last_name)
        body = loader.render_to_string(template_path, template_context)
        return {"to": [recipient.email],
                "subject": subject,
                "body": body}

    def _cancelling_party_name(self):
        if is_employee(self.user):
            return "MassChallenge Staff"
        else:
            return self.user.full_name()


def formatted_success_notification(office_hour):
    finalist_name = office_hour.finalist.full_name()
    mentor_name = office_hour.mentor.full_name()
    time_info = office_hour_time_info(office_hour)
    return SUCCESS_NOTIFICATION.format(finalist_name=finalist_name,
                                       mentor_name=mentor_name,
                                       date=time_info['date'],
                                       time=time_info['start_time'])
