from django.urls import reverse

from impact.tests.api_test_case import APITestCase
from impact.v1.views import ReserveOfficeHourView
from accelerator.tests.factories import MentorProgramOfficeHourFactory
from accelerator.tests.contexts import UserRoleContext
from accelerator.models import UserRole

class TestReserveOfficeHourView(APITestCase):
    view = ReserveOfficeHourView
    success_header = ReserveOfficeHourView.SUCCESS_HEADER
    fail_header = ReserveOfficeHourView.FAIL_HEADER
    
    def test_finalist_reserves_office_hour_success(self):
        # a finalist reserves an office hour, gets success response
        pass

    def test_finalist_reserves_office_hour_timecard(self):
        # a finalist reserves an office hour, gets timecard details in response
        pass

    def test_finalist_reserves_office_hour_gets_confirmation_email(self):
        # a finalist reserves and office hour, gets a confirmation email
        pass
    
    def test_previously_reserved_office_hour_gets_failure(self):
        # a finalist reserves a reserved office hour, gets failure response
        pass

    def test_reserve_on_behalf_of_success(self):
        # staff reserves a session on behalf of finalist, gets success
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id)
        self.assert_ui_notification(response, True, self.view.SUCCESS_DETAIL)

    def test_reserve_on_behalf_of_finalist_gets_email_notification(self):    
        # staff reserves a session on behalf of finalist, finalist is
        # notified by email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id)
        self.assert_notified(finalist)


    def test_reserve_on_behalf_of_finalist_mentor_gets_email_notification(self):    
        # staff reserves a session on behalf of finalist, mentor is
        # notified by email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id)
        self.assert_notified(office_hour.mentor)


    def post_response(self,
                      office_hour_id,
                      user_id=None,
                      startup_id=None,
                      request_user=None):
        request_user = request_user or self.staff_user()
        
        request_user.set_password("password")
        request_user.save()
        url = reverse(self.view.view_name)
        data = {'office_hour_id': office_hour_id}
        if user_id:
            data['user_id'] = user_id
        if startup_id:
            data['startup_id'] = startup_id
        with self.login(request_user):
            return self.post(url, data=data)

        
def _finalist():
    return UserRoleContext(UserRole.FINALIST).user
