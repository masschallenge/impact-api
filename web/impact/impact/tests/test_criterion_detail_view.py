from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_data_is_consistent_with_instance
from impact.tests.factories import CriterionFactory
from impact.v1.views import CriterionDetailView
from impact.v1.views.utils import valid_keys_note
from django.urls import reverse


class TestCriterionDetailView(APITestCase):
    view = CriterionDetailView

    def test_get(self):
        criterion = CriterionFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[criterion.id])
            response = self.client.get(url)
            assert_data_is_consistent_with_instance(response.data, criterion)

    def test_patch_object_exists(self):
        criterion = CriterionFactory()
        data = {'name': 'Patched Criterion',
                'type': 'sans serif',
                'judging_round_id': 1}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[criterion.id])
            self.client.patch(url, data)
            criterion.refresh_from_db()
            assert_data_is_consistent_with_instance(data, criterion)

    def test_patch_no_such_object(self):
        criterion = CriterionFactory()
        criterion_id = criterion.id
        criterion.delete()
        data = {'name': 'Patched Criterion',
                'type': 'sans serif',
                'judging_round_id': 1}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[criterion_id])
            response = self.client.patch(url, data)
            self.assertEqual(response.status_code, 404)

    def test_patch_bad_key_in_data(self):
        criterion = CriterionFactory()
        data = {'name': 'Patched Criterion',
                'type': 'sans serif',
                'judging_round_id': 1,
                'bad_key': 'B flat minor'}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[criterion.id])
            response = self.client.patch(url, data)
            note = valid_keys_note(self.view.helper_class.INPUT_KEYS)
            assert note in str(response.content)

    def test_patch_options(self):
        criterion = CriterionFactory()
        patch_options = {"id": {"type": "integer",
                                "readOnly": True,
                                "required": True},
                         "name": {"type": "string"},
                         "type": {"type": "string"},
                         "judging_round_id": {"type": "integer"}}
        self.assert_options_include("PATCH", patch_options,
                                    object_id=criterion.id)
