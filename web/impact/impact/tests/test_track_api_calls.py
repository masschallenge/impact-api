from django.test import (
    TestCase,
)

from mock import mock, patch

from impact.tests.api_test_case import APITestCase


class TestTrackAPICalls(APITestCase):
    @patch('impact.middleware.track_api_calls.TrackAPICalls.process_request.logger')
    def test_when_user_authenticated(self, logger_info_patch):
        with self.login(email=self.basic_user().email):
            response = self.client.get(/)
            logger_info_patch.info.assert_called_with()


    def test_when_no_user_authenticated(self):
        pass
