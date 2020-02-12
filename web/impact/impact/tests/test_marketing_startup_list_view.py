# -*- coding: utf-8 -*-
import json
import nose.tools as nt

from future import standard_library
from io import BytesIO as StringIO
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse

from accelerator_abstract.models.base_program_startup_status import (
    BADGE_STARTUP_LIST,
)
from .attributes import marketingapi
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import (
    EntrepreneurProfileFactory,
    ProgramFactory,
    ProgramStartupStatusFactory,
    SiteFactory,
    SiteProgramAuthorizationFactory,
    StartupFactory,
    StartupStatusFactory,
    StartupTeamMemberFactory,
)
from impact.v1.views import MarketingStartupListView
from impact.v1.views.marketing_startup_profile_view import (
    DEFAULT_PROFILE_TEXT_COLOR,
    DEFAULT_PROFILE_BACKGROUND_COLOR,
)

standard_library.install_aliases()


def get_temporary_image(filename):

    io = StringIO()
    size = (2, 2)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='PNG')
    image_file = InMemoryUploadedFile(io, None, filename, 'png', io.len, None)
    image_file.seek(0)
    return image_file


@marketingapi
class TestStartupList(APITestCase):

    def setUp(self):
        self.json_response = lambda url, params: json.loads(
            self.client.get(
                url, params).content)

    def test_200_if_have_permission(self):
        site = SiteFactory()
        program = ProgramFactory()
        response = self.client.get('/api/v1/startup_list_json_view/',
                                    {'site_name': site.name,
                                    'program_key': program.name})
        nt.assert_equal(response.status_code, 401)
        with self.login(email=self.basic_user().email):
            SiteProgramAuthorizationFactory(
                site=site,
                program=program,
                startup_list=True,
                startup_profile_base_url="http://test_base_url.com/")
            response = self.client.get('/api/v1/startup_list_json_view/',
                                        {'site_name': site.name,
                                        'program_key': program.name})
            nt.assert_equal(response.status_code, 200)

            second_program = ProgramFactory()
            SiteProgramAuthorizationFactory(
                site=site,
                program=second_program,
                startup_list=True,
                startup_profile_base_url="http://test_base_url.com/")
            response = self.client.get(
                '/api/v1/startup_list_json_view/',
                {'site_name': site.name,
                 'program_key': [program.name, second_program.name, ]})
            nt.assert_equal(response.status_code, 200)

    def test_group_by(self):
        with self.login(email=self.basic_user().email):
            site = SiteFactory()
            program = ProgramFactory()
            good = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='good',
                status_group='rating',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=2)
            poor = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='poor',
                status_group='rating',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=3)
            atrocious = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='atrocious',
                status_group='rating',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=5)
            dreadful = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='dreadful',
                status_group='rating',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=4)
            wonderful = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='wonderful',
                status_group='rating',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=1)
            othergroup = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='othergroup',
                status_group='unrelated',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=15)
            ungrouped = ProgramStartupStatusFactory(
                program=program,
                startup_list_include=True,
                startup_status='ungrouped',
                badge_display=BADGE_STARTUP_LIST,
                sort_order=13)

            letters = ('alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
                    'golf', 'hotel', 'india', 'juliet', 'kilo', 'lima',
                    'mike', 'november', 'oscar', 'papa')
            startups = dict((
                letter[0],
                StartupFactory(name=letter)) for letter in letters)
            for s in list(startups.values()):
                StartupStatusFactory.create(program_startup_status=ungrouped,
                                            startup=s)
            rated_wonderful = list(startups.values())[6]
            StartupStatusFactory.create(
                program_startup_status=atrocious,
                startup=rated_wonderful)
            StartupStatusFactory.create(
                program_startup_status=wonderful,
                startup=rated_wonderful)
            StartupStatusFactory.create(
                program_startup_status=dreadful,
                startup=rated_wonderful)
            StartupStatusFactory.create(
                program_startup_status=good,
                startup=rated_wonderful)
            StartupStatusFactory.create(
                program_startup_status=poor,
                startup=rated_wonderful)
            rated_poor = list(startups.values())[5]
            StartupStatusFactory.create(
                program_startup_status=atrocious,
                startup=rated_poor)
            StartupStatusFactory.create(
                program_startup_status=dreadful,
                startup=rated_poor)
            StartupStatusFactory.create(
                program_startup_status=poor,
                startup=rated_poor)
            StartupStatusFactory.create(
                program_startup_status=othergroup,
                startup=rated_poor)
    
            SiteProgramAuthorizationFactory(
                site=site,
                program=program,
                startup_list=True,
                startup_profile_base_url="http://test_base_url.com/")
            data = self.json_response(
                '/api/v1/startup_list_json_view/',
                {'site_name': site.name,
                'program_key': program.name,
                'group_by': "status_group:{0}".format("rating")})

            print("***********************", data)

            groups = dict((group['group_title'], group['startups'])
                        for group in data['groups'])
            nt.assert_equal(set(['poor', 'wonderful', 'All']), set(groups.keys()))
            nt.assert_equal(rated_poor.name, groups['poor'][0]['name'])
            nt.assert_equal(set(['poor', 'othergroup', 'ungrouped']),
                            set([status['status_name']
                                for status in groups['poor'][0]['statuses']]))
            nt.assert_equal(rated_wonderful.name, groups['wonderful'][0]['name'])
            nt.assert_equal(
                set(['wonderful', 'ungrouped']),
                set([status['status_name']
                    for status in groups['wonderful'][0]['statuses']]))

        # rated_poor_2 = list(startups.values())[3]
        # StartupStatusFactory.create(
        #     program_startup_status=atrocious,
        #     startup=rated_poor_2)
        # StartupStatusFactory.create(
        #     program_startup_status=dreadful,
        #     startup=rated_poor_2)
        # StartupStatusFactory.create(
        #     program_startup_status=poor,
        #     startup=rated_poor_2)
        # StartupStatusFactory.create(
        #     program_startup_status=othergroup,
        #     startup=rated_poor_2)

        # with self.login(email=self.basic_user().email):
        #     data = self.json_response(
        #         '/api/v1/startup_list_json_view/',
        #         {'site_name': site.name,
        #         'program_key': program.name,
        #         'order_by': 'AlphaAsc',
        #         'group_by': "StatusGroup:{0}".format("rating")})
        #     groups = dict((group['group_title'], group['startups'])
        #                 for group in data['groups'])
        #     nt.assert_equal(rated_poor_2.name, groups['poor'][0]['name'])
        #     nt.assert_equal(rated_poor.name, groups['poor'][1]['name'])
        #     nt.assert_equal([startup['name'][0] for startup in groups['All']], [
        #                     l for l in u'abcdefghijklmnop'])

    # def test_include_in_list_of_startups(self):
    #     site = SiteFactory()
    #     program = ProgramFactory()
    #     pss_true = ProgramStartupStatusFactory(
    #         program=program,
    #         startup_list_include=True,
    #         startup_list_tab_id='list',
    #         startup_status='pss_list')
    #     pss_false = ProgramStartupStatusFactory(
    #         program=program,
    #         startup_list_include=False,
    #         startup_list_tab_id='dont_list',
    #         startup_status='pss_dont_list')

    #     startup_should_be_listed = StartupStatusFactory.create(
    #         program_startup_status=pss_true).startup
    #     startup_should_not_be_listed = StartupStatusFactory.create(
    #         program_startup_status=pss_false).startup

    #     SiteProgramAuthorizationFactory(
    #         site=site,
    #         program=program,
    #         startup_list=True,
    #         startup_profile_base_url="http://test_base_url.com/")

    #     data = self.json_response(
    #         '/api/v1/startup_list_json_view/',
    #         {'SiteName': site.name,
    #          'SecurityKey': site.security_key,
    #          'ProgramKey': program.name})
    #     nt.assert_in(
    #         startup_should_be_listed.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_not_in(
    #         startup_should_not_be_listed.name, [
    #             s['name'] for s in data['startups']])

    #     stealth_startup = StartupFactory(
    #         is_visible=False,
    #         name='stealth startup')
    #     pss_dont_include_stealth = ProgramStartupStatusFactory(
    #         program=program,
    #         startup_list_include=True,
    #         startup_list_tab_id='stealth_false',
    #         startup_status='pss_dont_include_stealth')
    #     StartupStatusFactory.create(
    #         startup=stealth_startup,
    #         program_startup_status=pss_dont_include_stealth)
    #     data = self.json_response('/api/v1/startup_list_json_view/',
    #                               {'SiteName': site.name,
    #                                'SecurityKey': site.security_key,
    #                                'ProgramKey': program.name})
    #     nt.assert_not_in(
    #         stealth_startup.name, [
    #             s['name'] for s in data['startups']])

    #     pss_include_stealth = ProgramStartupStatusFactory(
    #         program=program,
    #         startup_list_include=True,
    #         include_stealth_startup_names=True,
    #         startup_list_tab_id='stealth_true',
    #         startup_status='pss_include_stealth')
    #     StartupStatusFactory.create(
    #         startup=stealth_startup,
    #         program_startup_status=pss_include_stealth)
    #     data = self.json_response('/api/v1/startup_list_json_view/',
    #                               {'SiteName': site.name,
    #                                'SecurityKey': site.security_key,
    #                                'ProgramKey': program.name})
    #     nt.assert_in(
    #         stealth_startup.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_true(all(s['statuses'] == [] for s in data[
    #                    'startups'] if not s['is_visible']))
    #     nt.assert_true(all(s['profile_url'] == '' for s in data[
    #                    'startups'] if not s['is_visible']))

    #     pss_named_confusingly = ProgramStartupStatusFactory(
    #         program=program,
    #         startup_list_include=True,
    #         startup_status=pss_true.startup_list_tab_id)
    #     startup_confusing = StartupStatusFactory.create(
    #         program_startup_status=pss_named_confusingly).startup
    #     data = self.json_response(
    #         '/api/v1/startup_list_json_view/',
    #         {'SiteName': site.name,
    #          'SecurityKey': site.security_key,
    #          'ProgramKey': program.name,
    #          'StartupStatus': pss_true.startup_list_tab_id})
    #     nt.assert_in(
    #         startup_should_be_listed.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_not_in(
    #         startup_should_not_be_listed.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_not_in(
    #         startup_confusing.name, [
    #             s['name'] for s in data['startups']])

    #     response = self.client.get(
    #         '/api/v1/startup_list_json_view/',
    #         {'SiteName': site.name,
    #          'SecurityKey': site.security_key,
    #          'ProgramKey': program.name,
    #          'StartupStatus': pss_true.startup_list_tab_id + 'nonsense'})
    #     nt.assert_not_equal(response.status_code, 500)

    #     new_program = ProgramFactory()
    #     SiteProgramAuthorizationFactory(
    #         site=site,
    #         program=new_program,
    #         startup_list=True,
    #         startup_profile_base_url="http://test_base_url.com/")
    #     new_pss_true = ProgramStartupStatusFactory(
    #         program=new_program,
    #         startup_list_include=True,
    #         startup_list_tab_id='list',
    #         startup_status='new_pss_list')
    #     new_startup_should_be_listed = StartupStatusFactory.create(
    #         program_startup_status=new_pss_true).startup
    #     data = self.json_response(
    #         '/api/v1/startup_list_json_view/',
    #         {'SiteName': site.name,
    #          'SecurityKey': site.security_key,
    #          'ProgramKey': [new_program.name, program.name]})
    #     nt.assert_in(
    #         startup_should_be_listed.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_in(
    #         new_startup_should_be_listed.name, [
    #             s['name'] for s in data['startups']])

    #     new_program_dup = ProgramFactory()
    #     SiteProgramAuthorizationFactory(
    #         site=site,
    #         program=new_program_dup,
    #         startup_list=True,
    #         startup_profile_base_url="http://test_base_url.com/")
    #     new_pss_true_dup = ProgramStartupStatusFactory(
    #         program=new_program_dup,
    #         startup_list_include=True,
    #         startup_list_tab_id='list',
    #         startup_status='new_pss_list_dup')
    #     StartupStatusFactory.create(
    #         program_startup_status=new_pss_true_dup,
    #         startup=new_startup_should_be_listed)
    #     data = self.json_response(
    #         '/api/v1/startup_list_json_view/',
    #         {'SiteName': site.name,
    #          'SecurityKey': site.security_key,
    #          'ProgramKey': [new_program.name, new_program_dup.name]})
    #     nt.assert_in(
    #         new_startup_should_be_listed.name, [
    #             s['name'] for s in data['startups']])
    #     nt.assert_equal(1, len(data['startups']))

    # def test_status_sorting(self):
    #     pass


# @marketingapi
# class TestStartupProfile(APITestCase):

#     def setUp(self):
#         self.json_response = lambda url, params: json.loads(
#             self.client.post(
#                 url, params).content)

#     def test_200_if_have_permission(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         pss = ProgramStartupStatusFactory(program=program,
#                                           startup_list_include=True,
#                                           startup_list_tab_id='list',
#                                           startup_status='pss_list')
#         startup = StartupFactory()

#         response = self.client.post(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(response.status_code, 403)

#         SiteProgramAuthorizationFactory(
#             site=site,
#             program=program,
#             startup_profiles=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         response = self.client.post(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(response.status_code, 403)

#         StartupStatusFactory.create(
#             program_startup_status=pss,
#             startup=startup)
#         response = self.client.post(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(response.status_code, 200)
#         response = self.client.post('/api/startup/',
#                                     {'SiteName': site.name,
#                                      'SecurityKey': site.security_key,
#                                      'StartupKey': startup.pk})
#         nt.assert_equal(response.status_code, 200)

#         response = self.client.get(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(response.status_code, 405)

#     def test_profile_fields(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         pss = ProgramStartupStatusFactory(program=program,
#                                           startup_list_include=True,
#                                           startup_list_tab_id='list',
#                                           startup_status='pss_list')
#         startup = StartupFactory(profile_background_color='',
#                                  profile_text_color='')
#         SiteProgramAuthorizationFactory(
#             site=site,
#             program=program,
#             startup_profiles=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         StartupStatusFactory.create(
#             program_startup_status=pss,
#             startup=startup)

#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(
#             data['profile_background_color'],
#             '#' +
#             DEFAULT_PROFILE_BACKGROUND_COLOR)
#         nt.assert_equal(
#             data['profile_text_color'],
#             '#' +
#             DEFAULT_PROFILE_TEXT_COLOR)

#         startup.profile_background_color = 'aaf'
#         startup.save()
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(data['profile_background_color'], '#aaf')
#         nt.assert_equal(
#             data['profile_text_color'],
#             '#' +
#             DEFAULT_PROFILE_TEXT_COLOR)

#         startup.profile_text_color = '33aaff'
#         startup.save()
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(data['profile_background_color'], '#aaf')
#         nt.assert_equal(data['profile_text_color'], '#33aaff')

#     def test_relative_profile_website_url_is_externalized(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         pss = ProgramStartupStatusFactory(program=program,
#                                           startup_list_include=True,
#                                           startup_list_tab_id='list',
#                                           startup_status='pss_list')
#         startup = StartupFactory()
#         SiteProgramAuthorizationFactory(
#             site=site,
#             program=program,
#             startup_profiles=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         StartupStatusFactory.create(
#             program_startup_status=pss,
#             startup=startup)

#         startup.website_url = 'testing.com'
#         startup.save()

#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(data['website_url'], 'http://testing.com')
#         startup.website_url = 'https://secure.com'
#         startup.save()

#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(data['website_url'], 'https://secure.com')
#         startup.website_url = 'www.secure.com'
#         startup.save()

#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})

#     def test_status_ordering(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         good = ProgramStartupStatusFactory(
#             program=program,
#             startup_list_include=True,
#             startup_status='good',
#             status_group='rating',
#             sort_order=2,
#             badge_display='STARTUP_PROFILE')
#         dreadful = ProgramStartupStatusFactory(
#             program=program,
#             startup_list_include=True,
#             startup_status='dreadful',
#             status_group='rating',
#             badge_display='STARTUP_PROFILE',
#             sort_order=4)
#         othergroup = ProgramStartupStatusFactory(
#             program=program,
#             startup_list_include=True,
#             startup_status='othergroup',
#             status_group='unrelated',
#             badge_display='STARTUP_PROFILE', sort_order=1)
#         startup = StartupFactory(
#             profile_background_color='',
#             profile_text_color='')
#         SiteProgramAuthorizationFactory(
#             site=site,
#             program=program,
#             startup_profiles=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         StartupStatusFactory.create(
#             program_startup_status=othergroup,
#             startup=startup)
#         StartupStatusFactory.create(
#             program_startup_status=dreadful,
#             startup=startup)
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(set(s['status_name'] for s in data['statuses']),
#                         set([othergroup.startup_status,
#                              dreadful.startup_status]))
#         StartupStatusFactory.create(
#             program_startup_status=good,
#             startup=startup)
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(set(s['status_name'] for s in data['statuses']),
#                         set([othergroup.startup_status, good.startup_status]))

#     def test_include_team_members(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         pss = ProgramStartupStatusFactory(program=program,
#                                           startup_list_include=True,
#                                           startup_list_tab_id='list',
#                                           startup_status='pss_list')
#         startup = StartupFactory()
#         StartupStatusFactory.create(
#             program_startup_status=pss,
#             startup=startup)
#         StartupTeamMemberFactory(startup=startup)
#         SiteProgramAuthorizationFactory(
#             site=site,
#             program=program,
#             startup_profiles=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(data['team_members'], [])

#         program2 = ProgramFactory(name='Program 2')
#         pss2 = ProgramStartupStatusFactory(program=program2,
#                                            startup_list_include=True,
#                                            startup_list_tab_id='list',
#                                            startup_status='pss_list2')
#         StartupStatusFactory.create(
#             program_startup_status=pss2,
#             startup=startup)
#         SiteProgramAuthorizationFactory(
#             site=site, program=program2,
#             startup_profiles=True,
#             startup_team_members=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         data = self.json_response(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_not_equal(data['team_members'], [])

#     def test_startup_info_with_non_ascii_characters(self):
#         site = SiteFactory()
#         program = ProgramFactory()
#         pss = ProgramStartupStatusFactory(program=program,
#                                           startup_list_include=True,
#                                           startup_list_tab_id='list',
#                                           startup_status='pss_list')
#         url = '/media/profile_pics/-ä-e1392382439863-209x300.jpg'
#         startup = StartupFactory(
#             high_resolution_logo=url
#         )
#         StartupStatusFactory.create(
#             program_startup_status=pss,
#             startup=startup)
#         profile = EntrepreneurProfileFactory(image=url)
#         StartupTeamMemberFactory(
#             display_on_public_profile=True,
#             startup=startup,
#             user=profile.user)
#         SiteProgramAuthorizationFactory(
#             site=site, program=program,
#             startup_profiles=True,
#             startup_team_members=True,
#             startup_profile_base_url="http://test_base_url.com/")
#         response = self.client.post(
#             '/api/startup/',
#             {'SiteName': site.name,
#              'SecurityKey': site.security_key,
#              'StartupKey': startup.organization.url_slug})
#         nt.assert_equal(response.status_code, 200)
