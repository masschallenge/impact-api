import json
from accelerator.models import CriterionOptionSpec

from impact.v1.views.utils import valid_keys_note
from impact.v1.helpers.validators import INVALID_INTEGER_ERROR
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_data_is_consistent_with_instance
from impact.tests.factories import (
    CriterionOptionSpecFactory,
    CriterionFactory,
)
from impact.v1.views import CriterionOptionSpecListView
from django.urls import reverse


class TestCriterionOptionSpecListView(APITestCase):
    view = CriterionOptionSpecListView

    def test_get(self):
        CriterionOptionSpec.objects.all().delete()
        option_specs = CriterionOptionSpecFactory.create_batch(5)
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.get(url)
            data = json.loads(response.content)
            results = {result['id']: result for result in data['results']}
            for spec in option_specs:
                assert results[spec.id]['option'] == spec.option

    def test_post_new_object(self):
        criterion = CriterionFactory()
        data = {'option': 'Posted Option',
                'weight': 1.5,
                'count': 1,
                'criterion_id': criterion.id}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.post(url, data)
            option_spec_id = json.loads(response.content)['id']
            option_spec = CriterionOptionSpec.objects.get(id=option_spec_id)
            assert_data_is_consistent_with_instance(data, option_spec)

    def test_post_bad_key_in_data(self):
        data = {'option': 'Posted Option',
                'weight': 1.5,
                'count': 1,
                'bad_key': 'B flat minor'}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.post(url, data)
            note = valid_keys_note(self.view.helper_class.INPUT_KEYS)
            assert note in str(response.content)

    def test_post_bad_int_in_int_field(self):
        criterion = CriterionFactory()
        data = {'option': 'Posted Option',
                'weight': 1.5,
                'count': 'one',
                'criterion_id': criterion.id}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.post(url, data)
            error = INVALID_INTEGER_ERROR.format(field='count',
                                                 value='one')
            assert error in str(response.content)

    def test_post_options(self):
        post_options = {"option": {"type": "string",
                                   "required": True},
                        "weight": {"type": "number"},
                        "count": {"type": "integer"},
                        "criterion_id": {"type": "integer",
                                         "required": True}}
        self.assert_options_include("POST", post_options)
