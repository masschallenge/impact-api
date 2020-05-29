from datetime import (
    datetime,
    timedelta,
)

from pytz import utc

from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import (
    Count,
    F,
)

from . import ImpactView
from accelerator.models import MentorProgramOfficeHour
User = get_user_model()

ISO_8601_DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(1)
ONE_WEEK = timedelta(8)


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
                 'start_date_time').annotate(finalist_count=Count("finalist"))

        self.response_elements['calendar_data'] = office_hours.values(
            "id",
            "start_date_time",
            "end_date_time",
            "mentor__last_name",
            "mentor__first_name",
            "mentor__expertprofile__title",
            "description",
            "topics",
            "finalist__first_name",
            "finalist__last_name",
            reserved=F("finalist_count"),
        )

        self.response_elements['timezones'] = office_hours.order_by(
            "location__timezone").values_list(
                "location__timezone", flat=True).distinct()
        self.succeed()

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
