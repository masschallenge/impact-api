from datetime import (datetime,
                      timedelta,
)
from django.urls import reverse

from accelerator.tests.factories import MentorProgramOfficeHourFactory

from impact.tests.api_test_case import APITestCase
from impact.v1.views import OfficeHoursCalendarView


class TestOfficeHoursCalendarView(APITestCase):
    view_name = OfficeHoursCalendarView.view_name
    
    def test_no_date_specified_sees_current_week(self):
        office_hour = self.create_office_hour()
        response = self.get_response(user=office_hour.mentor)
        self.assert_hour_in_response(response, office_hour)

    def create_office_hour(self,
                           mentor=None,
                           finalist=None,
                           start_date_time=None,
                           duration_minutes=30):
        create_params = {}
        if mentor:
            create_params=mentor
        duration=timedelta(duration_minutes)            
        start_date_time = start_date_time or datetime.now()
        end_date_time = start_date_time + duration
        create_params['start_date_time'] = start_date_time
        create_params['end_date_time'] = end_date_time
        return MentorProgramOfficeHourFactory(**create_params)

    def assert_hour_in_response(self, response, hour):
        response_data = response.data['calendar_data']
        self.assertIn(hour.id, [response_hour['id']
                                for response_hour in response_data])

    def get_response(self, user=None, data=None):
        user = user or self.staff_user()
        user.set_password("password")
        user.save()
        url = reverse(self.view_name)
        data = {} or data
        with self.login(email=user.email):
            return self.get(url, data=data)
        
    def test_no_date_specified_does_not_see_last_week(self):
        pass
    
    def test_sees_correct_range_when_date_specified(self):
        pass
    
    def test_mentor_with_hours_sees_hours_in_range(self):
        pass

    def test_mentor_with_hours_does_not_see_hours_out_of_range(self):
        pass

    def test_mentor_sees_hours_in_sorted_order(self):
        pass

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

    

    
    
