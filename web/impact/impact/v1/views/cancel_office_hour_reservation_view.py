from django.contrib.auth import get_user_model
from rest_framework.response import Response

from impact.minimal_email_handler import MinimalEmailHandler as email_handler
from impact.v1.views.impact_view import ImpactView

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import MentorProgramOfficeHour

User = get_user_model()


class CancelOfficeHourReservationView(ImpactView):
    view_name = "cancel_office_hours_reservation"

    def post(self, request):
        office_hour_id = request.POST.get("office_hour_id")
        message = request.POST.get("message")
        requesting_user_id = request.POST.get("user_id")
        requesting_user = User.objects.get(id=requesting_user_id)
        office_hour = MentorProgramOfficeHour.objects.get(pk=office_hour_id)
        success = False
        if _can_cancel(requesting_user, office_hour):
            emails = _prepare_email_notifications(office_hour,
                                                  message,
                                                  requesting_user)
            _cancel_reservation(office_hour)
            for email in emails:
                _send_email(email)
            success = True
        return Response({"success": success})


def _can_cancel(user, office_hour):
    return is_employee(user) or user == office_hour.finalist


def _cancel_reservation(office_hour):
    office_hour.finalist = None
    office_hour.save()


def _send_email(email_details):
    email_handler(**email_details).send()


def _prepare_email_notifications(office_hour,
                                 message,
                                 requesting_user):
    return []
