from pytz import timezone

from django.core import mail
from django.urls import reverse

from mc.models import UserRole
from accelerator.tests.contexts import UserRoleContext
from accelerator.tests.utils import days_from_now

from .api_test_case import APITestCase
from .factories import MentorProgramOfficeHourFactory
from ..permissions.v1_api_permissions import DEFAULT_PERMISSION_DENIED_DETAIL
from ..v1.views.cancel_office_hour_session_view import (
    DEFAULT_TIMEZONE,
    FAIL_HEADER,
    OFFICE_HOUR_SESSION_404,
    MENTOR_NOTIFICATION,
    PERMISSION_DENIED,
    STAFF_NOTIFICATION,
    SUCCESS_HEADER,
    CancelOfficeHourSessionView,
    MentorProgramOfficeHour,
)


class TestCancelOfficeHourSession(APITestCase):
    fail_header = FAIL_HEADER
    success_header = SUCCESS_HEADER
    url = reverse(CancelOfficeHourSessionView.view_name)

    def test_mentor_can_cancel_their_own_unreserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor, finalist=None
        )
        self._cancel_office_hour_session(office_hour.id, mentor)
        self.assert_office_hour_session_was_cancelled(office_hour)

    def test_mentor_can_cancel_their_own_unreserved_past_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            start_date_time=days_from_now(-3),
            mentor=mentor, finalist=None)
        self._cancel_office_hour_session(office_hour.id, mentor)
        self.assert_office_hour_session_was_cancelled(office_hour)

    def test_mentor_cancel_their_own_unreserved_session_ui_notification(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor, finalist=None)
        response = self._cancel_office_hour_session(office_hour.id, mentor)
        self.assert_mentor_cancel_reservation_ui_notification(
            office_hour, response
        )

    def test_mentor_cannot_cancel_their_own_reserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor)
        response = self._cancel_office_hour_session(office_hour.id, mentor)
        self.assert_ui_notification(response, False, PERMISSION_DENIED)

    def test_mentor_cannot_cancel_someone_else_unreserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        mentor2 = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            finalist=None,
            mentor=mentor2)
        self._cancel_office_hour_session(office_hour.id, mentor)
        self.assert_office_hour_session_was_not_cancelled(office_hour)

    def test_staff_can_cancel_unreserved_office_hour(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._cancel_office_hour_session(office_hour.id, self.staff_user())
        self.assert_office_hour_session_was_cancelled(office_hour)

    def test_mentor_receives_email_when_admin_cancels_unreserved_session(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        self._cancel_office_hour_session(office_hour.id, self.staff_user())
        self.assertEqual(mail.outbox[0].to, [office_hour.mentor.email])

    def test_staff_can_cancel_reserved_office_hour(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._cancel_office_hour_session(office_hour.id, self.staff_user())
        self.assert_office_hour_session_was_cancelled(office_hour)

    def test_mail_is_sent_to_attendees_on_reserved_session_cancellation(self):
        office_hour = MentorProgramOfficeHourFactory()
        self._cancel_office_hour_session(office_hour.id, self.staff_user())
        attendees_email = [email.to[0] for email in mail.outbox]
        to_addresses = [office_hour.mentor.email,
                        office_hour.finalist.email]
        self.assertEqual(set(attendees_email), set(to_addresses))

    def test_mail_includes_message_when_cancelled_session_has_message(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        message = 'cancelled due to conflicting meetings'
        self._cancel_office_hour_session(office_hour.id,
                                         self.staff_user(), message)
        self.assertIn(message, mail.outbox[0].alternatives[0][0])

    def test_mentor_received_email_when_they_cancel_their_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor, finalist=None
        )
        self._cancel_office_hour_session(office_hour.id, mentor)
        self.assertEqual(mail.outbox[0].to, [mentor.email])

    def test_staff_cancel_office_hour_session_ui_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        response = self._cancel_office_hour_session(office_hour.id,
                                                    self.staff_user())
        self.assert_staff_cancel_reservation_ui_notification(
            office_hour, response
        )

    def test_office_hour_session_not_existing_ui_notification(self):
        response = self._cancel_office_hour_session(0, self.staff_user())
        self.assert_ui_notification(response, False, OFFICE_HOUR_SESSION_404)

    def test_none_staff_or_none_mentor_ui_notification(self):
        office_hour = MentorProgramOfficeHourFactory()
        response = self._cancel_office_hour_session(office_hour.id,
                                                    self.basic_user())
        notification = {'detail': DEFAULT_PERMISSION_DENIED_DETAIL}
        self.assertEqual(response.data, notification)

    def assert_office_hour_session_was_cancelled(self, office_hour):
        self.assertFalse(MentorProgramOfficeHour.objects.filter(
            pk=office_hour.id).exists())

    def assert_office_hour_session_was_not_cancelled(self, office_hour):
        self.assertTrue(MentorProgramOfficeHour.objects.filter(
            pk=office_hour.id).exists())

    def assert_mentor_cancel_reservation_ui_notification(
            self, office_hour, response):
        context = self._get_office_hour_context(office_hour)
        self.assert_ui_notification(
            response, True, MENTOR_NOTIFICATION.format(**context))

    def assert_staff_cancel_reservation_ui_notification(self,
                                                        office_hour,
                                                        response):
        context = self._get_office_hour_context(office_hour)
        self.assert_ui_notification(
            response, True, STAFF_NOTIFICATION.format(**context))

    def _get_office_hour_context(self, office_hour):
        tz = timezone(office_hour.location.timezone or DEFAULT_TIMEZONE)
        start_date_time = office_hour.start_date_time
        date = start_date_time.astimezone(tz).strftime('%A, %d %B, %Y')
        start_time = start_date_time.astimezone(tz).strftime('%I:%M%p')
        end_time = office_hour.end_date_time.astimezone(tz).strftime('%I:%M%p')
        return {
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'mentor_name': office_hour.mentor.get_profile().full_name(),
        }

    def _expert_user(self, role):
        user = UserRoleContext(role).user
        user.set_password('password')
        user.save()
        return user

    def _cancel_office_hour_session(self, office_hour_id, user, msg=''):
        with self.login(email=user.email):
            return self.client.post(self.url, {
                'id': office_hour_id,
                'message': msg
            })
