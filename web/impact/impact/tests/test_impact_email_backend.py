from mock import patch
from django.test import TestCase

from ..minimal_email_handler import MinimalEmailHandler


# This definition of IMPACT_EMAIL_BACKEND duplicates a value in settings.py,
# but is necessary since the value is not included in the settings for test.
# See AC-7670 for more.
IMPACT_BACKEND_PATH = ".".join(["api.web.impact.impact",
                                "impact_email_backend",
                                "ImpactEmailBackend"])
ADD_LOGGING_HEADERS = IMPACT_BACKEND_PATH + "._add_logging_headers"


class TestEmailBackend(TestCase):

    @patch(ADD_LOGGING_HEADERS)
    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_sending_email_hits_backend(
        self,
        mocked_backend,
        mock_add_logging_headers
    ):
        with self.settings(
                SES_CONFIGURATION_SET="test",
                EMAIL_BACKEND=IMPACT_BACKEND_PATH):
            MinimalEmailHandler(["a@example.com"],
                                "subject",
                                "body").send()
            self.assertTrue(mocked_backend.called)

    @patch(ADD_LOGGING_HEADERS)
    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_email_contains_header_if_ses_config_set(
        self,
        mocked_backend,
        mock_add_logging_headers
    ):
        with self.settings(
                SES_CONFIGURATION_SET="test",
                EMAIL_BACKEND=IMPACT_BACKEND_PATH):
            MinimalEmailHandler(["a@example.com"],
                                "subject",
                                "body").send()
            self.assertTrue(mock_add_logging_headers.called)

    @patch(ADD_LOGGING_HEADERS)
    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_email_does_not_contain_header_if_ses_config_not_set(
        self,
        mocked_backend,
        mock_add_logging_headers
    ):
        with self.settings(
                SES_CONFIGURATION_SET="",
                EMAIL_BACKEND=IMPACT_BACKEND_PATH):
            MinimalEmailHandler(["a@example.com"],
                                "subject",
                                "body").send()
            self.assertFalse(mock_add_logging_headers.called)
