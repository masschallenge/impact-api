from django.urls import reverse

from impact.tests.api_test_case import APITestCase
from impact.v1.views import ReserveOfficeHourView
from ..permissions.v1_api_permissions import DEFAULT_PERMISSION_DENIED_DETAIL
from accelerator.tests.factories import MentorProgramOfficeHourFactory
from accelerator.tests.contexts import UserRoleContext
from accelerator.models import UserRole

class TestReserveOfficeHourView(APITestCase):
    view = ReserveOfficeHourView
    success_header = ReserveOfficeHourView.SUCCESS_HEADER
    fail_header = ReserveOfficeHourView.FAIL_HEADER
    
    def test_finalist_reserves_office_hour_success(self):
        # a finalist reserves an office hour, gets success response
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
        self.assert_ui_notification(response, True, self.view.SUCCESS_DETAIL)


    def test_finalist_reserves_office_hour_timecard(self):
        # a finalist reserves an office hour, gets timecard details in response
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
#        self.assert_response_contains_session_details(response)

    def test_finalist_reserves_office_hour_gets_confirmation_email(self):
        # a finalist reserves and office hour, gets a confirmation email
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
        self.assert_notified(finalist)

    
    def test_previously_reserved_office_hour_gets_failure(self):
        # a finalist reserves a reserved office hour, gets failure response
        office_hour = MentorProgramOfficeHourFactory()
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      request_user=finalist)
        self.assert_ui_notification(response,
                                    False,
                                    self.view.OFFICE_HOUR_ALREADY_RESERVED)
        

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

    def test_non_staff_reserve_on_behalf_of_failure(self):
        # finalist reserves a session on behalf of finalist, gets failure
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        finalist = _finalist()
        response = self.post_response(office_hour.id,
                                      finalist.id,
                                      request_user=_finalist())
        self.assert_ui_notification(response,
                                    False,
                                    DEFAULT_PERMISSION_DENIED_DETAIL)

        

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

def _mentor():
    return UserRoleContext(UserRole.MENTOR).user
    
