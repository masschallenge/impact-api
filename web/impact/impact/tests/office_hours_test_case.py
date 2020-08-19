from .api_test_case import APITestCase


class OfficeHoursTestCase(APITestCase):

    def assert_ui_notification(self, response, success, notification,
                               office_hour=None):
        data = response.data
        detail = notification if notification else ""
        header = self.ui_header(success, office_hour)
        self.assertTrue(all([
            data['success'] == success,
            data['header'] == header,
            data['detail'] == detail
        ]), msg='Notification data was not as expected')

    def ui_header(self, success, office_hour):
        if success:
            return self.success_header.format(mentor_name(office_hour))
        else:
            return self.fail_header


def mentor_name(office_hour):
    if office_hour and office_hour.mentor:
        return office_hour.mentor.full_name()
    return None
