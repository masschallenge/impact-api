import json
from accelerator.models import Criterion
from impact.v1.views.utils import valid_keys_note
from impact.tests.api_test_case import APITestCase
from impact.tests.utils import assert_data_is_consistent_with_instance
from impact.tests.factories import CriterionFactory
from impact.v1.views import CriterionListView
from django.urls import reverse


class TestCriterionListView(APITestCase):

    def test_get(self):
        Criterion.objects.all().delete()
        criteria = CriterionFactory.create_batch(5)
        with self.login(email=self.basic_user().email):
            url = reverse(CriterionListView.view_name)
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
            url = reverse(CriterionListView.view_name)
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
            url = reverse(CriterionListView.view_name)
            response = self.client.post(url, data)
            note = valid_keys_note(CriterionListView.helper_class.INPUT_KEYS)
            assert note in str(response.content)
