from django.template import loader
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import (
    MentorProgramOfficeHour,
    Startup,
)

from ...permissions.v1_api_permissions import (
    DEFAULT_PERMISSION_DENIED_DETAIL,
    IsAuthenticated,
)
from .impact_view import ImpactView
from .utils import (
    email_template_path,
    is_office_hour_reserver,
    localized_office_hour_start_time,
)
from ...minimal_email_handler import send_email
User = get_user_model()


mentor_template_name = "reserve_office_hour_email_to_mentor.html"
finalist_template_name = "reserve_office_hour_email_to_finalist.html"


class ReserveOfficeHourView(ImpactView):
    view_name = "reserve_office_hour"
    permission_classes = [IsAuthenticated]

    SUCCESS_HEADER = "Office Hours session reserved"
    SUCCESS_DETAIL = "You have reserved this office hour session"
    FAIL_HEADER = "Fail header"
    NO_OFFICE_HOUR_SPECIFIED = "No office hour was specified"
    NO_SUCH_OFFICE_HOUR = "No such office hour exists."
    NO_SUCH_STARTUP = "No such startup exists"
    NO_SUCH_USER = "No such user exists"
    OFFICE_HOUR_ALREADY_RESERVED = "That session has already been reserved"
    SUBJECT = "Office Hours Reservation Notification"
    STARTUP_NOT_ASSOCIATED_WITH_USER = ("The selected startup is not a valid "
                                        "choice for {}")
    USER_CANNOT_RESERVE_OFFICE_HOURS = ("The selected user is not allowed to "
                                        "reserve office hour sessions.")

    def post(self, request):
        '''
        params:
        office_hour_id (required)
        user_id (optional, defaults to request.user)
        startup_id (optional)

        '''
        (self._extract_request_data(request) and
         self._reserve_office_hour())
        return self._response()

    def _extract_request_data(self, request):
        if not (self._extract_office_hour(request) and
                self._extract_user(request) and
                self._extract_startup(request)):
            return False
        self.message = request.data.get("message", "")
        return True

    def _extract_office_hour(self, request):
        office_hour_id = request.data.get("office_hour_id", None)
        if office_hour_id is None:
            self.fail(self.NO_OFFICE_HOUR_SPECIFIED)
            return False
        try:
            self.office_hour = MentorProgramOfficeHour.objects.get(
                pk=office_hour_id)
        except MentorProgramOfficeHour.DoesNotExist:
            self.fail(self.NO_SUCH_OFFICE_HOUR)
            return False
        return True

    def _extract_user(self, request):
        user_id = request.data.get("user_id", None)
        if user_id is not None and user_id != request.user.id:
            try:
                self.target_user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                self.fail(self.NO_SUCH_USER)
                return False
            if is_employee(request.user):
                self.on_behalf_of = True
            else:
                self.fail(DEFAULT_PERMISSION_DENIED_DETAIL)
                return False
        else:
            self.target_user = request.user
            self.on_behalf_of = False
        if not is_office_hour_reserver(self.target_user):
            self.fail(self.USER_CANNOT_RESERVE_OFFICE_HOURS)
            return False
        return True

    def _extract_startup(self, request):
        startup_id = request.data.get("startup_id", None)
        if startup_id is None:
            self.startup = None
        else:
            try:
                self.startup = Startup.objects.get(pk=startup_id)
            except Startup.DoesNotExist:
                self.fail(self.NO_SUCH_STARTUP)
                return False
            if not self.target_user.startupteammember_set.filter(
                    startup=self.startup).exists():
                self.fail(self.STARTUP_NOT_ASSOCIATED_WITH_USER.format(
                    self.target_user.email))
                return False
        return True

    def _reserve_office_hour(self):
        if self.office_hour.finalist is not None:
            self.fail(self.OFFICE_HOUR_ALREADY_RESERVED)
            return False
        self._update_office_hour_data()
        self._send_confirmation_emails()
        self._succeed()
        return True

    def _update_office_hour_data(self):
        self.office_hour.finalist = self.target_user
        self.office_hour.description = self.message
        self.office_hour.startup = self.startup
        self.office_hour.save()

    def _send_confirmation_emails(self):
        mentor = self.office_hour.mentor
        finalist = self.target_user
        send_email(**self.prepare_email_notification(mentor,
                                                     finalist,
                                                     mentor_template_name))
        send_email(**self.prepare_email_notification(finalist,
                                                     mentor,
                                                     finalist_template_name))

    def prepare_email_notification(self,
                                   recipient,
                                   counterpart,
                                   template_name):
        template_path = email_template_path(template_name)
        if self.startup:
            startup_name = self.startup.organization.name
        else:
            startup_name = ""

        start_time = localized_office_hour_start_time(self.office_hour)
        context = {"recipient": recipient,
                   "counterpart": counterpart,
                   "office_hour_date_time": start_time,
                   "startup": startup_name,
                   "message": self.message}
        body = loader.render_to_string(template_path, context)
        return {"to": [recipient.email],
                "subject": self.SUBJECT,
                "body": body}

    def _succeed(self):
        if self.office_hour.startup:
            startup_name = self.office_hour.startup.organization.name
        else:
            startup_name = ""
        self.success = True
        self.header = self.SUCCESS_HEADER
        self.detail = self.SUCCESS_DETAIL
        self.timecard_info = {
            "finalist_first_name": self.target_user.first_name,
            "finalist_last_name": self.target_user.last_name,
            "topics": self.message,
            "startup": startup_name}

    def fail(self, detail):
        self.success = False
        self.header = self.FAIL_HEADER
        self.detail = detail
        self.timecard_info = {}

    def _response(self):
        return Response({
            'success': self.success,
            'header': self.header,
            'detail': self.detail,
            'timecard_info': self.timecard_info})