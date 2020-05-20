from mock import patch

from .api_test_case import APITestCase


class TestTrackAPICalls(APITestCase):
    @patch('impact.middleware.track_api_calls.logger')
    def test_when_user_authenticated(self, logger_patch):
        email = self.basic_user().email
        expected = {
            'user': email,
            'path': '/',
            'uri': 'http://testserver/',
            'is_ajax': False,
        }

        with self.login(email=email):
            self.client.get('/')
            logger_patch.info.assert_called_with(expected)

    @patch('impact.middleware.track_api_calls.logger')
    def test_when_no_user_authenticated(self, logger_patch):
        expected = {
            'user': None,
            'path': '/',
            'uri': 'http://testserver/',
            'is_ajax': False,
        }

        self.client.get('/')
        logger_patch.info.assert_called_with(expected)
