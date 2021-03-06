from pytz import timezone

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.template import loader

from rest_framework.response import Response
from add2cal import Add2Cal

from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import (
    MentorProgramOfficeHour,
    Startup,
)

from ...permissions.v1_api_permissions import (
    RESERVE_PERMISSION_DENIED_DETAIL,
    IsAuthenticated,
)
from ...views import ADD2CAL_DATE_FORMAT
from .impact_view import ImpactView
from .utils import (
    email_template_path,
    is_office_hour_reserver,
    office_hour_time_info,
    datetime_is_in_past,
)
from ...minimal_email_handler import send_email
User = get_user_model()


mentor_template_name = "reserve_office_hour_email_to_mentor.html"
finalist_template_name = "reserve_office_hour_email_to_finalist.html"
ICS_FILENAME = 'reminder.ics'
ICS_FILETYPE = 'text/calendar'


class ReserveOfficeHourView(ImpactView):
    view_name = "reserve_office_hour"
    permission_classes = [IsAuthenticated]

    OFFICE_HOUR_TITLE = "Office Hours Session with {}"
    SUCCESS_HEADER = "Office Hour reserved with {}"
    SUCCESS_PAST_DETAIL = ("This office officehour occurs in the past")
    FAIL_HEADER = "Office hour could not be reserved"
    NO_OFFICE_HOUR_SPECIFIED = "No office hour was specified"
    NO_SUCH_OFFICE_HOUR = "This office hour is no longer available."
    NO_SUCH_STARTUP = "No such startup exists"
    NO_SUCH_USER = "No such user exists"
    OFFICE_HOUR_ALREADY_RESERVED = "That session has already been reserved"
    SUBJECT = "Office Hours Reservation Notification"
    STARTUP_NOT_ASSOCIATED_WITH_USER = ("The selected startup is not a valid "
                                        "choice for {}")
    USER_CANNOT_RESERVE_OFFICE_HOURS = ("The selected user is not allowed to "
                                        "reserve office hour sessions.")
    CONFLICT_EXISTS = ("The requested time overlaps with another "
                       "existing officehours")

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
                self.fail(RESERVE_PERMISSION_DENIED_DETAIL)
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
        if self._conflict_exists():
            self.fail(self.CONFLICT_EXISTS)
            return False
        self._update_office_hour_data()
        self._send_confirmation_emails()
        self._succeed()
        return True

    def _conflict_exists(self):
        start = self.office_hour.start_date_time
        end = self.office_hour.end_date_time

        start_conflict = (Q(start_date_time__gt=start) &
                          Q(start_date_time__lt=end))
        end_conflict = (Q(end_date_time__gt=start) &
                        Q(end_date_time__lt=end))
        enclosing_conflict = (Q(start_date_time__lte=start) &
                              Q(end_date_time__gte=end))

        if self.target_user.finalist_officehours.filter(
                start_conflict | end_conflict | enclosing_conflict).exists():
            return True
        return False

    def _update_office_hour_data(self):
        self.office_hour.finalist = self.target_user
        self.office_hour.topics = self.message
        self.office_hour.startup = self.startup
        self.office_hour.save()

    def _send_confirmation_emails(self):
        mentor = self.office_hour.mentor
        finalist = self.target_user
        send_email(**self.prepare_email_notification(mentor,
                                                     finalist,
                                                     mentor_template_name,
                                                     True))
        send_email(**self.prepare_email_notification(finalist,
                                                     mentor,
                                                     finalist_template_name))

    def prepare_email_notification(self,
                                   recipient,
                                   counterpart,
                                   template_name,
                                   mentor_recipient=False):
        template_path = email_template_path(template_name)
        if self.startup:
            startup_name = self.startup.organization.name
        else:
            startup_name = ""
        self.mentor_recipient = mentor_recipient
        context = {"recipient": recipient,
                   "counterpart": counterpart,
                   "startup": startup_name,
                   "message": self.message,
                   "calendar_data": self.get_calendar_data(counterpart)
                   }
        context.update(office_hour_time_info(self.office_hour))
        html_email = loader.render_to_string(template_path, context)
        return {"to": [recipient.email],
                "subject": self.SUBJECT,
                "body": None,
                "attachment": (ICS_FILENAME,
                               self.calendar_data['ical_content'],
                               ICS_FILETYPE),
                "attach_alternative": (html_email, 'text/html')
                }

    def _succeed(self):
        if self.office_hour.startup:
            startup_name = self.office_hour.startup.organization.name
        else:
            startup_name = ""
        self.success = True
        self.header = self.SUCCESS_HEADER.format(
            self.office_hour.mentor.full_name())
        self.detail = self._get_detail()
        self.timecard_info = {
            "finalist_first_name": self.target_user.first_name,
            "finalist_last_name": self.target_user.last_name,
            "finalist_email": self.target_user.email,
            "topics": self.message,
            "startup": startup_name,
            "calendar_data": self.get_calendar_data(self.office_hour.mentor),
        }

    def _get_detail(self):
        start_date_time = self.office_hour.start_date_time
        if datetime_is_in_past(start_date_time):
            return self.SUCCESS_PAST_DETAIL
        else:
            return ""

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

    def get_calendar_data(self, counterpart_name):
        if hasattr(self, "calendar_data"):
            return self.calendar_data
        name = counterpart_name
        if self.mentor_recipient:
            name = self.startup.name if self.startup else counterpart_name
        title = self.OFFICE_HOUR_TITLE.format(name)
        office_hour = self.office_hour
        tz_str = ""
        if office_hour.location is None:
            tz_str = "UTC"
            location = ""
        else:
            tz_str = office_hour.location.timezone
            location = office_hour.location
        tz = timezone(tz_str)
        meeting_info = office_hour.meeting_info
        separator = ';' if office_hour.location and meeting_info else ""
        location_info = "{location}{separator}{meeting_info}"
        location_info = location_info.format(location=location,
                                             separator=separator,
                                             meeting_info=meeting_info)
        self.calendar_data = Add2Cal(
            start=office_hour.start_date_time.astimezone(tz).strftime(
                ADD2CAL_DATE_FORMAT),
            end=office_hour.end_date_time.astimezone(tz).strftime(
                ADD2CAL_DATE_FORMAT),
            title=title,
            description=self._get_description(counterpart_name),
            location=location_info,
            timezone=tz).as_dict()
        return self.calendar_data

    def _get_description(self, counterpart_name):
        topics_block = ""
        attendees_block = """
        Attendees:\n- {mentor_email}\n- {finalist_email} - {finalist_phone}\n
        """
        finalist = self.startup if self.startup else counterpart_name
        if self.office_hour.topics:
            topics_block = "Message from {finalist}:\n{topics}\n".format(
                topics=self.office_hour.topics,
                finalist=finalist)
        mentor_email = self.office_hour.mentor.email
        finalist_email = self.target_user.email
        finalist_phone = self.target_user.user_phone()
        attendees_block = attendees_block.format(mentor_email=mentor_email,
                                                 finalist_email=finalist_email,
                                                 finalist_phone=finalist_phone)
        description = """
        {attendees_block}

        {topics_block}
        """
        return description.format(topics_block=topics_block,
                                  attendees_block=attendees_block)
