from datetime import (
    datetime,
    timedelta,
)

from pytz import utc

from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import (
    BooleanField,
    Case,
    Count,
    F,
    Q,
    When,
    Value,
)
from . import ImpactView
from mc.models import (
    MentorProgramOfficeHour,
    UserRole,
)

User = get_user_model()

ISO_8601_DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(1)
ONE_WEEK = timedelta(8)

OFFICE_HOUR_HOLDER_ROLES = [UserRole.MENTOR, UserRole.AIR]

OFFICE_HOURS_HOLDER = Q(
    program_role__user_role__name__in=OFFICE_HOUR_HOLDER_ROLES)
ACTIVE_PROGRAM = Q(program_role__program__program_status='active')


class OfficeHoursCalendarView(ImpactView):
    permission_classes = []
    view_name = "office_hours_calendar_view"
    SUCCESS_HEADER = "Office hours fetched successfully"
    FAILURE_HEADER = "Office hours could not be fetched"
    BAD_DATE_SPEC = "We were unable to parse the date specifier"
    NO_SUCH_USER = "We were not able to locate that user"

    def fail(self, detail):
        self.response_elements['success'] = False
        self.response_elements['header'] = self.FAILURE_HEADER
        self.response_elements['detail'] = detail
        self.response_elements['calendar_data'] = None

    def succeed(self):
        self.response_elements['success'] = True
        self.response_elements['header'] = self.SUCCESS_HEADER

    def _get_target_user(self, request):
        user_id = request.query_params.get("user_id", None)
        if user_id is None:
            self.target_user = request.user
        else:
            try:
                self.target_user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                self.fail(self.NO_SUCH_USER)
                return False
        return True

    def _get_start_date(self, request):
        date_spec = request.query_params.get("date_spec", None)

        try:
            self.start_date = start_date(date_spec)
        except ValueError:
            self.fail(self.BAD_DATE_SPEC)
            return False
        return True

    def _get_office_hours_data(self):
        end_date = self.start_date + ONE_WEEK + 2 * ONE_DAY
        office_hours = MentorProgramOfficeHour.objects.filter(
             mentor=self.target_user,
             start_date_time__range=[self.start_date, end_date]).order_by(
                 'start_date_time').annotate(
                     finalist_count=Count("finalist")).annotate(
                         reserved=Case(
                             When(finalist_count__gt=0, then=Value(True)),
                             default=Value(False),
                             output_field=BooleanField()))

        primary_industry_key = "mentor__expertprofile__primary_industry__name"
        self.response_elements['calendar_data'] = office_hours.values(
            "id",
            "mentor_id",
            "finalist_id",
            "start_date_time",
            "end_date_time",
            "description",
            "topics",
            "startup_id",
            "reserved",
            "meeting_info",
            location_name=F("location__name"),
            location_timezone=F("location__timezone"),
            finalist_first_name=F("finalist__first_name"),
            finalist_last_name=F("finalist__last_name"),
            mentor_title=F("mentor__expertprofile__title"),
            mentor_company=F("mentor__expertprofile__company"),
            mentor_first_name=F("mentor__first_name"),
            mentor_last_name=F("mentor__last_name"),
            mentor_primary_industry=F(primary_industry_key),
            startup_name=F("startup__organization__name"),
        )
        self.response_elements['location_choices'] = self.location_choices()
        self.response_elements['timezones'] = office_hours.order_by(
            "location__timezone").values_list(
                "location__timezone", flat=True).distinct()
        self.response_elements['location_choices'] = self.location_choices()
        program_families = self.mentor_program_families()
        self.response_elements['mentor_program_families'] = program_families
        self.succeed()

    def mentor_program_families(self):
        return self.target_user.programrolegrant_set.filter(
            OFFICE_HOURS_HOLDER and ACTIVE_PROGRAM).values_list(
                "program_role__program__program_family__name",
                flat=True).distinct()

    def location_choices(self):
        location_path = "__".join(["program_role",
                                   "program",
                                   "program_family",
                                   "programfamilylocation",
                                   "location"])
        location_name = location_path + "__name"
        location_id = location_path + "__id"
        location_choices = self.target_user.programrolegrant_set.filter(
            OFFICE_HOURS_HOLDER and
            ACTIVE_PROGRAM).values_list(
                location_name, location_id)
        return location_choices.distinct()

    def get(self, request):
        self.response_elements = {}
        (self._get_target_user(request) and
         self._get_start_date(request) and
         self._get_office_hours_data())
        return Response(self.response_elements)


def start_date(date_spec=None):
    # return the latest monday that is less than or equal to today
    # throws ValueError if date_spec is not in ISO-8601 format

    # note: this function will become more involved when we allow for
    # user-specified start-of-week

    if date_spec:
        initial_date = datetime.strptime(date_spec, ISO_8601_DATE_FORMAT)
    else:
        initial_date = datetime.now()

    # This calculation depends on the fact that monday == 0 in python

    start_date = initial_date - timedelta(initial_date.weekday())
    adjusted_start_date = start_date - ONE_DAY
    return utc.localize(adjusted_start_date)
