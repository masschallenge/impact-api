import json

from django.urls import reverse

from accelerator.models import Criterion
from impact.v1.views.utils import valid_keys_note
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_data_is_consistent_with_instance
from impact.tests.factories import CriterionFactory
from impact.v1.views import CriterionListView
from impact.v1.helpers import INVALID_INTEGER_ERROR


class TestCriterionListView(APITestCase):
    view = CriterionListView

    def test_get(self):
        Criterion.objects.all().delete()
        criteria = CriterionFactory.create_batch(5)
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.get(url)
            data = json.loads(response.content)
            results = {result['id']: result for result in data['results']}
            for criterion in criteria:
                assert results[criterion.id]['name'] == criterion.name

    def test_post_new_object(self):
        data = {'name': 'Posted Criterion',
                'type': 'sans serif',
                'judging_round_id': 1}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.post(url, data)
            criterion_id = json.loads(response.content)['id']
            criterion = Criterion.objects.get(id=criterion_id)
            assert_data_is_consistent_with_instance(data, criterion)

    def test_post_bad_key_in_data(self):
        data = {'name': 'Posted Criterion',
                'type': 'sans serif',
                'judging_round_id': 1,
                'bad_key': 'B flat minor'}
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            response = self.client.post(url, data)
            note = valid_keys_note(self.view.helper_class.INPUT_KEYS)
            assert note in str(response.content)

    def test_post_options(self):
        post_options = {"name": {"type": "string",
                                 "required": True},
                        "type": {"type": "string",
                                 "required": True},
                        "judging_round_id": {"type": "integer",
                                             "required": True}}
        self.assert_options_include("POST", post_options)

    def test_filter_by_judging_round(self):
        criterion = CriterionFactory()
        judging_round_id = criterion.judging_round_id
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            url += "?judging_round_id={}".format(judging_round_id)
            response = self.client.get(url)
            results = json.loads(response.content)['results']
            self.assertEqual(len(results), 1)
            for key, val in results[0].items():
                self.assertEqual(val, getattr(criterion, key))

    def test_filter_id_by_non_int_value(self):
        judging_round_id = "seventeen"
        with self.login(email=self.basic_user().email):
            url = reverse(self.view.view_name)
            url += "?judging_round_id={}".format(judging_round_id)
            response = self.client.get(url)
            error = INVALID_INTEGER_ERROR.format(field='judging_round_id',
                                                 value=judging_round_id)
            self.assertIn(error, str(response.content))
