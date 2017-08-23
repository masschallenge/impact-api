from impact.tests.api_test_case import APITestCase
from impact.tests.factories import PartnerFactory


class TestPartner(APITestCase):

    def test_str(self):
        partner = PartnerFactory()
        assert str(partner) == partner.name

    def test_partner_twitter_handle_is_from_organization(self):
        partner = PartnerFactory()
        partner.twitter_handle = 'partner'
        self.assertEqual(
            partner.twitter_handle,
            partner.organization.twitter_handle)

    def test_partner_website_url_is_from_organization(self):
        partner = PartnerFactory()
        partner.website_url = 'http://test.com'
        self.assertEqual(
            partner.website_url,
            partner.organization.website_url)
