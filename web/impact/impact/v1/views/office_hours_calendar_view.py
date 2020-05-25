from datetime import (date,
                      datetime,
                      timedelta,
)

from rest_framework.response import Response
from . import ImpactView
from impact.permissions.v1_api_permissions import (
    OfficeHourFinalistPermission,
    OfficeHourMentorPermission,
)

ISO_8601_DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(1)

class OfficeHoursCalendarView(ImpactView):
    permission_classes = [OfficeHourFinalistPermission | OfficeHourMentorPermission]
    view_name = "office_hours_calendar_view"

    def fail(self, detail):
        self.success = False
        self.header = SUCCESS_HEADER
        self.detail = detail
        self.calendar_data = None
        
    def _get_target_user(self, request):
        user_id = request.data.get("user_id", None)
        if user_id is None:
            self.target_user = request.user
        else:
            try:
                self.target_user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                self.fail(NO_SUCH_USER)                
                return False
        return True

    def _get_start_date(self, request):
        date_spec = request.data.get("date_spec", None)

        try: 
            self.start_date = start_date(date_spec)

        except ValueError:
            self.fail(BAD_DATE_SPEC)
            return False
        return True

    def _get_office_hours_calendar_data(self):
         office_hours = MentorProgramOfficeHour.objects.filter(
             mentor = self.target_user,
             start_date_time__range=[self.start, self.end]).order_by(
                 'start_date_time')

         self.calendar_data = office_hours.values(
             "id",
             "start_date_time",
             "end_date_time", 
             "mentor__last_name"
             "mentor__last_name",
             "description",
             "topics",             
             "finalist__first_name",
             "finalist__last_name",
             "startup": F("startup__organization__name"),
             "reserved"=F("finalist_count"),
         )
             
         self.timezones = office_hours.order_by("location__timezone").values_list(
             "location__timezone", flat=True).distinct()
         
             
         
    def get(self, request):
        (self._get_target_user(request) and
         self._get_start_date() and
         self._get_office_hours_data())
        

        return self.response()

    def response(self):
        content = {"success": self.success,
                   "header": self.header,
                   "detail": self.detail}
        if self.calendar_data is not None:
            content['calendar_data'] = self.calendar_data
            content['timezones'] = self.timezones
        response =  Response(content)
        


def start_date(date_spec=None):
    # return the latest monday that is less than or equal to today
    # throws ValueError if date_spec is not in ISO-8601 format
    
    # note: this function will become more involved when we allow for user-specified
    # start-of-week
    
    if date_spec:
        initial_date = datetime.strptime(date_spec, ISO_8601_DATE_FORMAT).date()        
    else:
        initial_date = date.today()

    # This calculation depends on the fact that monday == 0 in python
    
    start_date =  initidal_date - datetime(initial_date.weekday())
    adjusted start_date = start_date - ONE_DAY
    return start_date

    
