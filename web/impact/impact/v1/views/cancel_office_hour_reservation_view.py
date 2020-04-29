from pytz import timezone

from django.contrib.auth import get_user_model
from django.template import loader

from rest_framework.response import Response

from impact.minimal_email_handler import MinimalEmailHandler as email_handler
from impact.v1.views.impact_view import ImpactView

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import MentorProgramOfficeHour

User = get_user_model()

mentor_template_name = "cancel_office_hour_reservation_email_to_mentor.html"
finalist_template_name = ("cancel_office_hour_reservation_email_to_finalist."
                          "html")
SUBJECT_LINE = "MassChallenge | Cancelled Office Hours with {} {}"


class CancelOfficeHourReservationView(ImpactView):
    view_name = "cancel_office_hours_reservation"

    def post(self, request):
        office_hour_id = request.POST.get("office_hour_id")
        message = request.POST.get("message", "")
        requesting_user_id = request.POST.get("user_id")
        requesting_user = User.objects.get(id=requesting_user_id)
        office_hour = MentorProgramOfficeHour.objects.get(pk=office_hour_id)
        success = False
        if _can_cancel(requesting_user, office_hour):
            _send_email(prepare_email_notification(office_hour,
                                                   requesting_user,
                                                   office_hour.finalist,
                                                   message,
                                                   office_hour.mentor,
                                                   mentor_template_name))
            _send_email(prepare_email_notification(office_hour,
                                                   requesting_user,
                                                   office_hour.mentor,
                                                   message,
                                                   office_hour.finalist,
                                                   finalist_template_name))
            _cancel_reservation(office_hour)
            success = True
        return Response({"success": success})


def _can_cancel(user, office_hour):
    return (office_hour.finalist is not None and
            (is_employee(user) or user == office_hour.finalist))


def _cancel_reservation(office_hour):
    office_hour.finalist = None
    office_hour.save()


def _send_email(email_details):
    email_handler(**email_details).send()


def prepare_email_notification(office_hour,
                               requesting_user,
                               counterpart,
                               message,
                               recipient,
                               template_name):
    template_path = _template_path(template_name)
    office_hour_date_time = _localize_start_time(office_hour)
    template_context = {"recipient": recipient,
                        "office_hour_date_time": office_hour_date_time,
                        "cancelling_party": requesting_user,
                        "custom_message": message}

    subject = SUBJECT_LINE.format(counterpart.first_name,
                                  counterpart.last_name)
    body = loader.render_to_string(template_path, template_context)
    return {"to": [recipient.email],
            "subject": subject,
            "body": body}


def _localize_start_time(office_hour):
    tz = timezone(office_hour.location.timezone)
    return office_hour.start_date_time.astimezone(tz)


def _template_path(template_name):
    return "emails/{}".format(template_name)
