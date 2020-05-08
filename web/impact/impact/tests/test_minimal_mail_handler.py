from django.test import TestCase
from django.core import mail
from .minimal_email_handler import MinimalEmailHandler


DEFAULT_PARAM_KEYS = ("to",
                      "subject",
                      "body")


DEFAULT_PARAM_VALS = (["a@example.com"],
                      "TEST SUBJECT",
                      "TEST BODY")


class TestMinimalEmailHandler(TestCase):
    def test_simple_email(self):
        params = email_params()
        email = send_email(params)
        self._assert_email_matches_expected_values(email, params)

    def test_email_with_sender_specified_is_sent(self):
        params = email_params(DEFAULT_PARAM_KEYS + ("from_email",),
                              DEFAULT_PARAM_VALS + ("c@example.com",))
        email = send_email(params)
        self._assert_email_matches_expected_values(email, params)

    def test_email_with_bcc_specified(self):
        params = email_params(DEFAULT_PARAM_KEYS + ("bcc",),
                              DEFAULT_PARAM_VALS + (["e@example.com"],))
        email = send_email(params)
        self._assert_email_matches_expected_values(email, params)

    def _assert_email_matches_expected_values(self, email, values_dict):
        for key, val in values_dict.items():
            self.assertEqual(val, getattr(email, key))


def send_email(params):
    MinimalEmailHandler(**params).send()
    return mail.outbox[-1]


def email_params(keys=DEFAULT_PARAM_KEYS,
                 vals=DEFAULT_PARAM_VALS):
    return dict(zip(keys, vals))
