from datetime import (
    datetime,
    timedelta,
)

import calendar

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
from ...utils import compose_filter
from ...permissions.v1_api_permissions import (
    IsAuthenticated,
)
from accelerator.models import (
    Clearance,
    MentorProgramOfficeHour,
    ProgramFamily,
    ProgramRoleGrant,
    UserRole,
    Location,
)
from accelerator_abstract.models.base_user_utils import is_employee
User = get_user_model()


ISO_8601_DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(1)
ONE_WEEK = timedelta(8)



STAFF = "staff"
MENTOR = "mentor"
FINALIST = "finalist"
NOT_ALLOWED = "not_allowed"
LOCATION_FIELDS = (
    'id',
    'street_address',
    'timezone',
    'country',
    'state',
    'name',
    'city',
)

OFFICE_HOUR_HOLDER_ROLES = [UserRole.MENTOR, UserRole.AIR]
OFFICE_HOUR_RESERVER_ROLES = [UserRole.FINALIST, UserRole.ALUM]
OFFICE_HOURS_HOLDER = Q(
    program_role__user_role__name__in=OFFICE_HOUR_HOLDER_ROLES)
OFFICE_HOURS_RESERVER = Q(
    program_role__user_role__name__in=OFFICE_HOUR_RESERVER_ROLES)
ACTIVE_PROGRAM = Q(program_role__program__program_status='active')


class OfficeHoursCalendarView(ImpactView):
    permission_classes = [IsAuthenticated]
    view_name = "office_hours_calendar_view"
    SUCCESS_HEADER = "Office hours fetched successfully"
    FAIL_HEADER = "Office hours could not be fetched"
    BAD_FOCAL_DATE = "We were unable to parse the date specifier"
    NO_SUCH_USER = "We were not able to locate that user"
    NOT_OFFICE_HOURS_VIEWER = ("You are not able to view office hours at this "
                               "time. Please see MassChallenge staff.")

    def get(self, request):
        self.response_elements = {}
        (self._get_target_user(request) and
         self._check_request_user_type() and
         self._get_date_range(request) and
         self._set_user_query() and
         self._get_office_hours_data(request))
        return Response(self.response_elements)

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

    def _check_request_user_type(self):
        """
        determine whether we are viewing as "staff", "mentor", or "finalist"
        if we pursue AC-7778, this will be modified to read from request data
        """
        if is_employee(self.target_user):
            self.request_user_type = STAFF
        elif _is_mentor(self.target_user):
            self.request_user_type = MENTOR
        elif _is_finalist(self.target_user):
            self.request_user_type = FINALIST
        else:
            self.request_user_type = NOT_ALLOWED
        return True

    def _get_date_range(self, request):
        focal_date = request.query_params.get("focal_date", None)
        calendar_span = request.query_params.get("calendar_span", "week")
        upcoming = bool(request.query_params.get("upcoming", False))

        try:
            self.start_date, self.end_date = _date_range(calendar_span, upcoming, focal_date)

        except ValueError:
            self.fail(self.BAD_FOCAL_DATE)
            return False
        return True

    def _office_hours_queryset(self):
        if self.request_user_type == STAFF:
            return self._staff_office_hours_queryset()
        elif self.request_user_type == MENTOR:

            return self._mentor_office_hours_queryset()
        elif self.request_user_type == FINALIST:
            return self._finalist_office_hours_queryset()
        else:
            self.response_elements['detail'] = self.NOT_OFFICE_HOURS_VIEWER
            return self._null_office_hours_queryset()

    def _staff_office_hours_queryset(self):
        staff_programs = Clearance.objects.clearances_for_user(
            self.target_user).values_list(
                "program_family", flat=True)
        in_visible_program_family = Q(
            program_role__program__program_family__in=staff_programs)
        program_mentors = ProgramRoleGrant.objects.filter(
            ACTIVE_PROGRAM &
            OFFICE_HOURS_HOLDER &
            in_visible_program_family).values_list(
                "person__id", flat=True)
        relevant_staff = _relevant_staff(staff_programs)
        mentors = list(program_mentors) + [self.target_user.id]
        active_mentors = Q(mentor__in=mentors)
        return MentorProgramOfficeHour.objects.filter(
            active_mentors | relevant_staff,
            start_date_time__range=[self.start_date, self.end_date]).order_by(
                'start_date_time').annotate(
                    finalist_count=Count("finalist")).annotate(
                        own_office_hour=Case(
                            When(mentor_id=self.target_user.id,
                                 then=Value(True)),
                            default=Value(False),
                            output_field=BooleanField()))

    def _mentor_office_hours_queryset(self):
        return MentorProgramOfficeHour.objects.filter(
            mentor=self.target_user,
            start_date_time__range=[self.start_date, self.end_date]).order_by(
            'start_date_time').annotate(
            finalist_count=Count("finalist")).annotate(
            own_office_hour=Case(
                default=Value(False),
                output_field=BooleanField()))

    def _finalist_office_hours_queryset(self):
        reserved_by_user = Q(finalist=self.target_user)
        unreserved = Q(finalist__isnull=True)
        user_programs = self.target_user.programrolegrant_set.filter(
            ACTIVE_PROGRAM & OFFICE_HOURS_RESERVER).values_list(
                "program_role__program", flat=True)
        relevant_staff = _relevant_staff(user_programs)
        relevant_mentors = Q(**compose_filter(("mentor",
                                               "programrolegrant",
                                               "program_role",
                                               "program",
                                               "in"),
                                              user_programs))
        return MentorProgramOfficeHour.objects.filter(
            (reserved_by_user |
             unreserved & (relevant_mentors | relevant_staff)),
            start_date_time__range=[self.start_date, self.end_date]).annotate(
                own_office_hour=Case(
                    default=Value(False),
                    output_field=BooleanField()))

    def _null_office_hours_queryset(self):
        return MentorProgramOfficeHour.objects.none().annotate(
            own_office_hour=Case(
                default=Value(False),
                output_field=BooleanField()))

    def _set_user_query(self):
        if self.request_user_type == STAFF:
            self.user_query = Clearance.objects.clearances_for_user(
                self.target_user).filter(
                program_family__programs__program_status='active')
            self.location_path = "__".join(["program_family",
                                            "programfamilylocation",
                                            "location"])
            self.program_family = "__".join(["program_family", "name"])
        else:
            self.user_query = self.target_user.programrolegrant_set.filter(
                OFFICE_HOURS_HOLDER & ACTIVE_PROGRAM)
            self.location_path = "__".join(["program_role",
                                            "program",
                                            "program_family",
                                            "programfamilylocation",
                                            "location"])
            self.program_family = "__".join(["program_role",
                                             "program",
                                             "program_family",
                                             "name"])
        return True

    def _get_office_hours_data(self, request):
        primary_industry_key = "mentor__expertprofile__primary_industry__name"
        office_hours = self._office_hours_queryset().filter(
            program__isnull=True).order_by(
            'start_date_time').annotate(
            finalist_count=Count("finalist")).annotate(
            reserved=Case(
                When(finalist_count__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()))

        if(request.query_params.get("upcoming", False)):
            office_hours = office_hours.filter(finalist__isnull=True)

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
            "own_office_hour",
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
            finalist_email=F("finalist__email"),
            mentor_email=F("mentor__email"),
            startup_primary_industry=F("startup__primary_industry__name"),
            startup_short_pitch=F("startup__short_pitch")
        )
        self.response_elements['timezones'] = office_hours.filter(
            location__isnull=False).order_by(
                "location__timezone").values_list("location__timezone",
                                                  flat=True).distinct()
        self.response_elements['location_choices'] = self.location_choices()
        program_families = self.mentor_program_families()
        self.response_elements['mentor_program_families'] = program_families
        self.response_elements['user_startups'] = self._user_startups()
        self.response_elements['user_type'] = self.request_user_type
        self.succeed()

    def _user_startups(self):
        return self.target_user.startupteammember_set.order_by(
            '-id').values(
                "startup_id",
                name=F("startup__organization__name")).distinct()

    def mentor_program_families(self):
        return self.user_query.values_list(
            self.program_family, flat=True).distinct()

    def location_choices(self):
        locations = self.user_query.filter(
            Q(**{self.location_path + '__isnull': False})
        ).values(**_location_lookups(self.location_path)).distinct()
        locations_list = list(locations)
        has_remote_location = _check_remote_location(locations_list)

        if not has_remote_location:
            remote_location_fields = dict([("location_" + field, F(field))
                                           for field in LOCATION_FIELDS])
            remote_loc = Location.objects.filter(
                name="Remote").values(**remote_location_fields).first()
            locations_list.append(remote_loc) if remote_loc else locations_list
        return locations_list

    def fail(self, detail):
        self.response_elements['success'] = False
        self.response_elements['header'] = self.FAIL_HEADER
        self.response_elements['detail'] = detail
        self.response_elements['calendar_data'] = None

    def succeed(self):
        self.response_elements['success'] = True
        self.response_elements['header'] = self.SUCCESS_HEADER


def _check_remote_location(locations_list):
    return any([loc['location_name'] == 'Remote' for loc in locations_list])


def _location_lookups(location_path):
    return dict([_location_dict_pair(field, location_path)
                 for field in LOCATION_FIELDS])


def _location_dict_pair(field, location_path):
    return (_format_key(field), _make_f_expression(field, location_path))


def _format_key(field):
    return "location_" + field


def _make_f_expression(field, location_path):
    return F("{}__{}".format(location_path, field))


def _date_range(calendar_span, upcoming, focal_date=None):
    # returns (start_date, end_date)
    # When calendar_span == week and upcoming == False
    # start_date is the latest monday that is less than or equal to today,
    # end_date is start_date + seven days
    # When calendar_span == month and upcoming == False
    # start_date is the first day of the new month
    # end_date is start_date + length of the current month
    # both values are then padded by 24 hours to allow for TZ differences
    # when upcoming == True
    # start_date is the current date period

    # throws ValueError if focal_date is not in ISO-8601 format

    if focal_date:
        initial_date = datetime.strptime(focal_date, ISO_8601_DATE_FORMAT)
    else:
        initial_date = datetime.now()

    if upcoming and initial_date < datetime.now():
        initial_date = datetime.now()

    initial_date = utc.localize(initial_date)
    if calendar_span == "month":
        
        elasped_time = timedelta(int(initial_date.strftime("%d")))
        month_start = initial_date - elasped_time
        days_in_month = calendar.monthrange(month_start.year, month_start.month)[1]
        one_month = timedelta(days_in_month + 1)
        # embedded asumption that only directory will ask for month span data
        # therefore we should return only upcoming office hours
        start_date = month_start + elasped_time
        end_date = month_start + one_month + ONE_DAY
    else:
        # This calculation depends on the fact that monday == 0 in python
        start_date = initial_date - timedelta(initial_date.weekday())
        end_date = start_date + ONE_WEEK + ONE_DAY
  
    adjusted_start_date = start_date - ONE_DAY
    return adjusted_start_date, end_date


def _is_mentor(user):
    return user.programrolegrant_set.filter(
        ACTIVE_PROGRAM & OFFICE_HOURS_HOLDER).exists()


def _is_finalist(user):
    return user.programrolegrant_set.filter(
        ACTIVE_PROGRAM & OFFICE_HOURS_RESERVER).exists()


def _relevant_staff(user_programs):
    program_families = ProgramFamily.objects.filter(programs__in=user_programs)
    staff_ids = Clearance.objects.filter(
        program_family_id__in=program_families).values_list(
            'user_id', flat=True)
    return Q(**compose_filter(('mentor',
                               'id',
                               'in'),
                              staff_ids))
