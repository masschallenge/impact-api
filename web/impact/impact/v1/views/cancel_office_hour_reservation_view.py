from pytz import timezone

from django.contrib.auth import get_user_model
from django.template import loader

from rest_framework.response import Response

from impact.minimal_email_handler import MinimalEmailHandler as email_handler
from impact.v1.views.impact_view import ImpactView
from impact.permissions.v1_api_permissions import (
    OfficeHourFinalistPermission,
)
from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import MentorProgramOfficeHour

User = get_user_model()

mentor_template_name = "cancel_office_hour_reservation_email_to_mentor.html"
finalist_template_name = ("cancel_office_hour_reservation_email_to_finalist."
                          "html")
SUBJECT_LINE = "MassChallenge | Cancelled Office Hours with {} {}"


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
        self.office_hour = MentorProgramOfficeHour.objects.get(
            pk=self.office_hour_id)
        success = False
        if self._can_cancel():
            _send_email(self.prepare_email_notification(self.office_hour.mentor,
                                                        self.office_hour.finalist,
                                                        mentor_template_name))
            _send_email(self.prepare_email_notification(self.office_hour.finalist,
                                                        self.office_hour.mentor,
                                                        finalist_template_name))
            self._cancel_reservation()
            success = True
        return Response({"success": success})

    def prepare_email_notification(self,
                                   recipient,
                                   counterpart,                                   
                                   template_name):
        template_path = _template_path(template_name)
        office_hour_date_time = _localize_start_time(self.office_hour)
        template_context = {"recipient": recipient,
                            "office_hour_date_time": office_hour_date_time,
                            "cancelling_party": self.user,
                            "custom_message": self.message}

        subject = SUBJECT_LINE.format(counterpart.first_name,
                                      counterpart.last_name)
        body = loader.render_to_string(template_path, template_context)
        return {"to": [recipient.email],
                "subject": subject,
                "body": body}

    def _can_cancel(self):
        return (self.office_hour.finalist is not None and
                (is_employee(self.user) or
                 self.user == self.office_hour.finalist))

    
    def _cancel_reservation(self):
        self.office_hour.finalist = None
        self.office_hour.save()

def _send_email(email_details):
    email_handler(**email_details).send()




def _localize_start_time(office_hour):
    tz = timezone(office_hour.location.timezone)
    return office_hour.start_date_time.astimezone(tz)


def _template_path(template_name):
    return "emails/{}".format(template_name)
