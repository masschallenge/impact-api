from django.core import mail

from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.v1.views import CancelOfficeHourReservationView

class TestCancelOfficeHourReservationView(APITestCase):
    def mentee_cancels_their_own_office_hour_reservation(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_reservation_cancelled(office_hour)

    def mentee_cancels_office_hour_reservation_and_gets_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.finalist)

    def mentee_cancels_office_hour_reservation_mentor_gets_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.mentor)

    def notification_includes_submitted_message(self):
        cancellation_message = "I'm sorry I had to cancel"
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour,
                                  user=office_hour.finalist,
                                  message=cancellation_message))
        self.assert_notified(office_hour.mentor,
                             message=cancellation_message)
        
    def staff_user_cancels_their_own_office_hour_reservation(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_reservation_cancelled(office_hour)

    def staff_user_cancels_office_hour_reservation_and_gets_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_notified(self.office_hour.finalist)

    def staff_user_cancels_office_hour_reservation_mentor_gets_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_notified(office_hour.mentor)
        
    
    def non_staff_user_attempts_to_cancel_reservation_not_theirs(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_reservation_not_cancelled(office_hour)

    def non_staff_user_attempts_to_cancel_reservation_not_theirs(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_not_notified(office_hour.mentor)                

    def user_attempts_to_cancel_non_existent_reservation(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._submit_cancellation(office_hour, user=self.basic_user())
        # assert what?
        
    def user_attempts_to_cancel_non_existent_reservation_no_notification(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_not_notified(office_hour.mentor)                
        

    def _submit_cancellation(self, office_hour, user, message=""):
        with self.login(email=user.email):
            url = reverse(CancelOfficeHourReservationView.view_name)
            data = {"office_hour_id": office_hour.id,
                    "message": message}
            response = self.client.post(url, data=data)
            return response

    def assert_notified(user, message=""):
        email = mail.outbox[-1]
        self.assertContains(email.to, user.email)
        if message:
            self.assertContains(email.body, message)
            
