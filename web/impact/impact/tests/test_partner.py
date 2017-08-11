from impact.tests.api_test_case import APITestCase
from impact.tests.factories import PartnerFactory


class TestPartner(APITestCase):
    def test_str(self):
        partner = PartnerFactory()
        assert str(partner) == partner.name
