from django.core import mail
from django.urls import reverse

from accelerator.models import UserRole
from accelerator.tests.contexts import UserRoleContext
from accelerator.tests.utils import days_from_now

from impact.tests.api_test_case import APITestCase
from impact.tests.factories import MentorProgramOfficeHourFactory
from impact.v1.views.cancel_office_hour_session_view import (
    CancelOfficeHourSessionView,
    get_office_hour_shared_context,
    get_ui_notification,
    MentorProgramOfficeHour,
    PERMISSION_DENIED,
)


class TestCancelOfficeHourSession(APITestCase):
    url = reverse(CancelOfficeHourSessionView.view_name)

    def test_mentor_can_cancel_their_own_unreserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor, finalist=None
        )
        with self.login(email=mentor.email):
            self.client.post(self.url, {
                'id': office_hour.id,
            })
            office_hour_count = MentorProgramOfficeHour.objects.filter(
                pk=office_hour.id).count()
            self.assertEqual(office_hour_count, 0)

    def test_mentor_can_cancel_their_own_unreserved_past_session(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            start_date_time=days_from_now(-3),
            mentor=mentor, finalist=None)
        with self.login(email=mentor.email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            context = get_office_hour_shared_context(office_hour)
            expected = get_ui_notification(context)
            self.assertEqual(response.data['detail'], expected)

    def test_mentor_cancel_their_own_unreserved_session_ui_notification(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor, finalist=None)
        with self.login(email=mentor.email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            context = get_office_hour_shared_context(office_hour)
            expected = get_ui_notification(context)
            self.assertEqual(response.data['detail'], expected)

    def test_mentor_cannot_cancel_their_own_reserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            mentor=mentor)
        with self.login(email=mentor.email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            self.assertEqual(response.data['detail'], PERMISSION_DENIED)

    def test_mentor_cannot_cancel_someone_else_unreserved_office_hour(self):
        mentor = self._expert_user(UserRole.MENTOR)
        mentor2 = self._expert_user(UserRole.MENTOR)
        office_hour = MentorProgramOfficeHourFactory(
            finalist=None,
            mentor=mentor2)
        with self.login(email=mentor.email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            self.assertEqual(response.status_code, 403)

    def test_staff_can_cancel_unreserved_office_hour(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        with self.login(email=self.staff_user().email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            context = get_office_hour_shared_context(office_hour)
            expected = get_ui_notification(context, staff=True)
            self.assertEqual(response.data['detail'], expected)

    def test_email_is_sent_mentor_when_admin_cancels_unreserved_session(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        with self.login(email=self.staff_user().email):
            self.client.post(self.url, {
                'id': office_hour.id,
            })
            self.assertEqual(mail.outbox[0].to, [office_hour.mentor.email])

    def test_staff_can_cancel_reserved_office_hour(self):
        office_hour = MentorProgramOfficeHourFactory()
        with self.login(email=self.staff_user().email):
            response = self.client.post(self.url, {
                'id': office_hour.id,
            })
            context = get_office_hour_shared_context(office_hour)
            expected = get_ui_notification(context, staff=True)
            self.assertEqual(response.data['detail'], expected)

    def test_mail_is_sent_to_attendees_on_reserved_session_cancellation(self):
        office_hour = MentorProgramOfficeHourFactory()
        with self.login(email=self.staff_user().email):
            self.client.post(self.url, {
                'id': office_hour.id,
            })
            attendees_email = [email.to[0] for email in mail.outbox]
            to_addresses = [office_hour.mentor.email,
                            office_hour.finalist.email]
            self.assertEqual(set(attendees_email), set(to_addresses))

    def test_mail_includes_message_when_cancelled_session_has_message(self):
        office_hour = MentorProgramOfficeHourFactory(finalist=None)
        with self.login(email=self.staff_user().email):
            message = 'cancelled due to conflicting meetings'
            self.client.post(self.url, {
                'id': office_hour.id,
                'message': message
            })
            self.assertIn(message, mail.outbox[0].alternatives[0][0])

    def _expert_user(self, role):
        user = UserRoleContext(role).user
        user.set_password('password')
        user.save()
        return user
