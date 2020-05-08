from .tests.api_test_case import APITestCase
from .tests.utils import assert_data_is_consistent_with_instance
from .tests.factories import (
    CriterionFactory,
    CriterionOptionSpecFactory,
)
from .v1.views import CriterionOptionSpecDetailView
from .v1.views.utils import valid_keys_note
from django.urls import reverse


class TestCriterionOptionSpecDetailView(APITestCase):
    view = CriterionOptionSpecDetailView

    def test_get(self):
        option_spec = CriterionOptionSpecFactory()
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[option_spec.id])
            response = self.client.get(url)
            assert_data_is_consistent_with_instance(response.data, option_spec)

    def test_patch_object_exists(self):
        option_spec = CriterionOptionSpecFactory()
        criterion = CriterionFactory()
        data = {'option': 'Patched Option',
                'weight': 1.5,
                'count': 1,
                'criterion_id': criterion.id}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[option_spec.id])
            self.client.patch(url, data)
            option_spec.refresh_from_db()
            assert_data_is_consistent_with_instance(data, option_spec)

    def test_patch_no_such_object(self):
        option_spec = CriterionOptionSpecFactory()
        option_spec_id = option_spec.id
        option_spec.delete()
        data = {'option': 'Patched Option',
                'weight': 1.5,
                'count': 1}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[option_spec_id])
            response = self.client.patch(url, data)
            self.assertEqual(response.status_code, 404)

    def test_patch_bad_key_in_data(self):
        option_spec = CriterionOptionSpecFactory()
        data = {'option': 'Patched Option',
                'weight': 1.5,
                'count': 1,
                'bad_key': 'B flat minor'}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name, args=[option_spec.id])
            response = self.client.patch(url, data)
            note = valid_keys_note(
                self.view.helper_class.INPUT_KEYS)
            assert note in str(response.content)

    def test_patch_options(self):
        option_spec = CriterionOptionSpecFactory()
        patch_options = {"id": {"type": "integer",
                                "readOnly": True,
                                "required": True},
                         "option": {"type": "string"},
                         "weight": {"type": "number"},
                         "count": {"type": "integer"},
                         "criterion_id": {"type": "integer"}}
        self.assert_options_include("PATCH", patch_options,
                                    object_id=option_spec.id)
