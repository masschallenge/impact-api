from datetime import (datetime,
                      timedelta,
)
from pytz import utc

from django.urls import reverse

from accelerator.tests.factories import MentorProgramOfficeHourFactory
from accelerator.tests.utils import days_from_now

from impact.tests.api_test_case import APITestCase
from impact.v1.views import (ISO_8601_DATE_FORMAT,
                             OfficeHoursCalendarView,
                             ONE_DAY,
)
                             


class TestOfficeHoursCalendarView(APITestCase):
    view_name = OfficeHoursCalendarView.view_name
    
    def test_no_date_specified_sees_current_week(self):
        office_hour = self.create_office_hour()
        response = self.get_response(user=office_hour.mentor)
        self.assert_hour_in_response(response, office_hour)

    def test_no_date_specified_does_not_see_last_week(self):
        office_hour = self.create_office_hour(
            start_date_time=days_from_now(-9))
        response = self.get_response(user=office_hour.mentor)
        self.assert_hour_not_in_response(response, office_hour)        
    
    def test_date_specified_sees_sessions_in_range(self):
        two_weeks_ago = days_from_now(-14)
        date_spec = two_weeks_ago.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour(
            start_date_time=two_weeks_ago)
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_hour_in_response(response, office_hour)        
        
    def test_date_specified_does_not_see_sessions_not_in_range(self):
        two_weeks_ago = days_from_now(-14)
        date_spec = two_weeks_ago.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour()
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_hour_not_in_response(response, office_hour)        

    def test_hours_returned_in_date_sorted_order(self):
        start_date_time = utc.localize(datetime(2020,1,31)) # a Wednesday
        date_spec = start_date_time.strftime(ISO_8601_DATE_FORMAT)
        office_hour = self.create_office_hour(start_date_time=start_date_time)
        self.create_office_hour(start_date_time=start_date_time-ONE_DAY,
                                mentor=office_hour.mentor)
        self.create_office_hour(start_date_time=start_date_time+ONE_DAY,
                                mentor=office_hour.mentor)
        response = self.get_response(user=office_hour.mentor,
                                     date_spec=date_spec)
        self.assert_sessions_sorted_by_date(response)
        

    def test_office_hour_has_correct_mentor_information(self):
        pass

    def test_office_hour_has_correct_finalist_information(self):
        pass

    def test_user_with_no_hours_sees_empty_response(self):
        pass

    def test_user_with_no_hours_sees_success_response(self):
        pass

    def test_user_with_no_hours_in_range_sees_empty_response(self):
        pass

    def test_user_with_no_hours_in_range_sees_success_response(self):
        pass

    def test_bad_date_spec_gets_fail_response(self):
        pass

    

    
    

    def create_office_hour(self,
                           mentor=None,
                           finalist=None,
                           start_date_time=None,
                           duration_minutes=30):
        create_params = {}
        if mentor:
            create_params['mentor'] = mentor
        duration=timedelta(duration_minutes)            
        start_date_time = start_date_time or datetime.now()
        end_date_time = start_date_time + duration
        create_params['start_date_time'] = start_date_time
        create_params['end_date_time'] = end_date_time
        return MentorProgramOfficeHourFactory(**create_params)

    def assert_hour_in_response(self, response, hour):
        self.assertTrue(check_hour_in_response(response, hour),
                        msg="The office hour session was not in the response")

    def assert_hour_not_in_response(self, response, hour):
        self.assertFalse(check_hour_in_response(response, hour),
                        msg="The office hour session was in the response")

    def assert_sessions_sorted_by_date(self, response):
        dates = [session['start_date_time']
                 for session in response.data['calendar_data']]
        self.assertEqual(dates, sorted(dates))
        
    def get_response(self,
                     user=None,
                     target_user_id=None,
                     date_spec=None):
        user = user or self.staff_user()
        user.set_password("password")
        user.save()
        url = reverse(self.view_name)
        data = {}
        if date_spec is not None:
            data['date_spec'] = date_spec
        if target_user_id is not None:
            data['user_id'] = target_user_id
        with self.login(email=user.email):
            return self.get(url, data=data)
       
def check_hour_in_response(response, hour):
    response_data = response.data['calendar_data']
    return hour.id in [response_hour['id'] 
                       for response_hour in response_data]
