from impact.tests.api_test_case import APITestCase
from impact.tests.factories import PartnerTeamMemberFactory


class TestPartnerTeamMember(APITestCase):

    def test_str(self):
        partner_team_member = PartnerTeamMemberFactory()
        assert str(partner_team_member.team_member) in str(partner_team_member)
        assert partner_team_member.partner.name in str(partner_team_member)
