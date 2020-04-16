from mock import patch
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from impact.minimal_email_handler import MinimalEmailHandler

class TestEmailBackend(TestCase):

    @patch("impact.impact_email_backend.ImpactEmailBackend._add_logging_headers")
    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_email_contains_header_if_ses_config_set(
        self,
        mocked_backend,
        mock_add_logging_headers
    ):
        with self.settings(
                SES_CONFIGURATION_SET="test",
                EMAIL_BACKEND='mc.email_backends.AccelerateEmailBackend'):
            MinimalEmailHandler(["a@example.com"],
                                "subject",
                                "body").send()
            self.assertTrue(mock_add_logging_headers.called)

    @patch("impact.impact_email_backend.ImpactEmailBackend._add_logging_headers")
    @patch("django.core.mail.backends.smtp.EmailBackend.send_messages")
    def test_email_does_not_contain_header_if_ses_config_not_set(
        self,
        mocked_backend,
        mock_add_logging_headers
    ):
        with self.settings(
                SES_CONFIGURATION_SET="",
                EMAIL_BACKEND='mc.email_backends.AccelerateEmailBackend'):
            MinimalEmailHandler(["a@example.com"],
                                "subject",
                                "body").send()
            self.assertFalse(mock_add_logging_headers.called)

        
