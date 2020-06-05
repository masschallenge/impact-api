from django.core import mail
from django.urls import reverse

from accelerator.tests.factories import (
    MentorProgramOfficeHourFactory,
)
from impact.tests.api_test_case import APITestCase
from impact.v1.views import (
    CancelOfficeHourReservationView,
    formatted_success_notification,
    NO_SUCH_RESERVATION,
    NO_SUCH_OFFICE_HOUR,
)

from impact.v1.views.cancel_office_hour_reservation_view import (
    FAIL_HEADER,
    SUCCESS_HEADER,
)


class TestCancelOfficeHourReservationView(APITestCase):
    fail_header = FAIL_HEADER
    success_header = SUCCESS_HEADER

    def test_finalist_cancels_their_own_office_hour_reservation(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_reservation_cancelled(office_hour)

    def test_finalist_cancels_and_gets_notification(self):
        '''A finalist cancelling their reservation should receive a
        notification'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.finalist)

    def test_finalist_cancels_and_gets_ui_notification(self):
        '''A finalist cancelling their reservation should receive a
        UI success notification'''
        office_hour = MentorProgramOfficeHourFactory()
        response = self._submit_cancellation(office_hour,
                                             user=office_hour.finalist)
        notification = formatted_success_notification(office_hour)
        self.assert_ui_notification(response, True, notification)

    def test_finalist_cancels_mentor_gets_notification(self):
        '''A finalist cancelling their reservation should trigger a
        notification to the mentor'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=office_hour.finalist)
        self.assert_notified(office_hour.mentor)

    def test_email_notification_includes_submitted_message(self):
        cancellation_message = "Sorry I had to cancel"
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

    def test_staff_user_cancels_reservation_gets_ui_notification(self):
        '''A staff user cancelling someone else's office hour should succeed'''
        office_hour = MentorProgramOfficeHourFactory()
        response = self._submit_cancellation(office_hour,
                                             user=self.staff_user())
        notification = formatted_success_notification(office_hour)
        self.assert_ui_notification(response, True, notification)

    def test_staff_user_cancels_nonexistent_reservation_ui_notification(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        response = self._submit_cancellation(office_hour,
                                             user=self.staff_user())
        self.assert_ui_notification(response, False, NO_SUCH_RESERVATION)

    def test_staff_user_cancels_nonexistent_hour_ui_notification(self):
        response = self._submit_cancellation(None,
                                             user=self.staff_user())
        self.assert_ui_notification(response, False, NO_SUCH_OFFICE_HOUR)

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
        self._submit_cancellation(office_hour, user=self.make_user())
        self.assert_reservation_not_cancelled(office_hour)

    def test_non_staff_user_not_finalist_no_notification(self):
        '''A non-staff user attempting to cancel someone else's reservation
        should not receive a notification'''
        office_hour = MentorProgramOfficeHourFactory()
        self._submit_cancellation(office_hour, user=self.make_user())
        self.assert_not_notified(office_hour.mentor)

    def test_user_attempts_to_cancel_non_existent_reservation(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        response = self._submit_cancellation(office_hour,
                                             user=self.make_user())
        notification = {
            'detail': NO_SUCH_RESERVATION,
            'header': FAIL_HEADER,
            'success': False}
        self.assertEqual(response.data, notification)

    def test_user_attempts_to_cancel_non_existent_hour(self):
        response = self._submit_cancellation(None,
                                             user=self.make_user())
        notification = {
            'detail': NO_SUCH_OFFICE_HOUR,
            'header': FAIL_HEADER,
            'success': False}
        self.assertEqual(response.data, notification)

    def test_user_cancels_non_existent_reservation_no_notification(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._submit_cancellation(office_hour, user=self.make_user())
        self.assert_not_notified(office_hour.mentor)

    def _submit_cancellation(self, office_hour, user, message=""):
        if office_hour is None:
            office_hour = MentorProgramOfficeHourFactory()
            office_hour_id = office_hour.id
            office_hour.delete()
        else:
            office_hour_id = office_hour.id
        user.set_password("password")
        user.save()

        with self.login(email=user.email):
            url = reverse(CancelOfficeHourReservationView.view_name)
            data = {"office_hour_id": office_hour_id,
                    "user_id": user.id,
                    "message": message}
            response = self.client.post(url, data=data)
        return response

    def assert_notified(self, user, message=""):
        emails = [email for email in mail.outbox if user.email in email.to]
        self.assertGreater(len(emails), 0)
        email = emails[0]
        if message:
            self.assertIn(message, email.body)

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
