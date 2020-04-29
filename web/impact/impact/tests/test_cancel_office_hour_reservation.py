from django.core import mail
from django.urls import reverse

from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
)

from impact.tests.api_test_case import APITestCase
from impact.v1.views import CancelOfficeHourReservationView


class TestCancelOfficeHourReservationView(APITestCase):
    def test_mentee_cancels_their_own_office_hour_reservation(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_reservation_cancelled(office_hour)

    def test_finalist_cancels_and_gets_notification(self):
        '''A finalist cancelling their reservation should receive a
        notification'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.finalist)

    def test_finalist_cancels_mentor_gets_notification(self):
        '''A finalist cancelling their reservation should trigger a
        notification to the mentor'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.mentor)

    def test_notification_includes_submitted_message(self):
        cancellation_message = "I'm sorry I had to cancel"
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour,
                                  user=office_hour.finalist,
                                  message=cancellation_message)
        self.assert_notified(office_hour.mentor,
                             message=cancellation_message)

    def test_staff_user_cancels_reservation(self):
        '''A staff user cancelling someone else's office hour should succeed'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_reservation_cancelled(office_hour)

    def test_staff_user_trigger_notification_mentor(self):
        '''A staff user cancelling someone else's office hour should trigger a
        notification to the mentor'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_notified(office_hour.mentor)

    def test_staff_user_trigger_notification_finalist(self):
        '''A staff user cancelling someone else's office hour should trigger a
        notification to the finalist'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.staff_user())
        self.assert_notified(office_hour.finalist)

    def test_non_staff_user_not_finalist_fails(self):
        '''A non-staff user attempting to cancel someone else's reservation
        should fail'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_reservation_not_cancelled(office_hour)

    def test_non_staff_user_not_finalist_no_notification(self):
        '''A non-staff user attempting to cancel someone else's reservation
        should not receive a notification'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_not_notified(office_hour.mentor)

    def test_user_attempts_to_cancel_non_existent_reservation(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._submit_cancellation(office_hour, user=self.basic_user())
        # assert what?

    def test_user_cancels_non_existent_reservation_no_notification(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._submit_cancellation(office_hour, user=self.basic_user())
        self.assert_not_notified(office_hour.mentor)

    def _submit_cancellation(self, office_hour, user, message=""):
        with self.login(email=self.basic_user().email):
            url = reverse(CancelOfficeHourReservationView.view_name)
            data = {"office_hour_id": office_hour.id,
                    "user_id": user.id,
                    "message": message}
            response = self.client.post(url, data=data)
        return response

    def assert_notified(self, user, message=""):
        self.assertGreater(len(mail.outbox), 0, msg="Outgoing mail empty")
        email = mail.outbox[-1]
        self.assertContains(email.to, user.email)
        if message:
            self.assertContains(email.body, message)

    def assert_not_notified(self, user):
        if mail.outbox:
            self.assertNotIn(user.email, [email.to for email in mail.outbox],
                             msg="Found an email sent to user")

    def assert_reservation_cancelled(self, office_hour):
        office_hour.refresh_from_db()
        self.assertIsNone(office_hour.finalist,
                          msg="Reservation was not cancelled")

    def assert_reservation_not_cancelled(self, office_hour):
        old_finalist = office_hour.finalist
        office_hour.refresh_from_db()
        self.assertEqual(office_hour.finalist,
                         old_finalist,
                         msg="Reservation was cancelled")
