# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import json
from django.urls import reverse

from accelerator.models import (
    StartupRole,
    UserRole
)
from accelerator_abstract.models import ACTIVE_PROGRAM_STATUS
from impact.graphql.middleware import NOT_LOGGED_IN_MSG
from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext
from impact.tests.factories import (
    ApplicationFactory,
    ExpertFactory,
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
    ProgramStartupStatusFactory,
    StartupMentorRelationshipFactory,
    StartupStatusFactory,
    UserRoleFactory,
    EntrepreneurFactory,
)
from impact.tests.utils import capture_stderr
from impact.graphql.query import (
    EXPERT_NOT_FOUND_MESSAGE,
    ENTREPRENEUR_NOT_FOUND_MESSAGE,
    NON_FINALIST_PROFILE_MESSAGE
)
from accelerator.tests.contexts import (
    StartupTeamMemberContext,
    UserRoleContext,
)

from impact.utils import get_user_program_and_startup_roles

MENTEE_FIELDS = """
    startup {
        id
        name
        highResolutionLogo
        shortPitch
    }
    program {
        family
        year
    }
"""


class TestGraphQL(APITestCase):
    url = reverse('graphql')
    auth_url = reverse('graphql-auth')

    def test_anonymous_user_cannot_access_main_graphql_view(self):
        user = ExpertFactory()
        query = """query {{ expertProfile(id: {id}) {{ title }} }}
            """.format(id=user.id)

        with capture_stderr(self.client.post,
                            self.url,
                            data={'query': query}) as (response, _):
            error_messages = [x['message'] for x in response.json()['errors']]

        self.assertIn(NOT_LOGGED_IN_MSG, error_messages)

    def test_anonymous_user_can_access_auth_graphql_view(self):
        query = """mutation {
                    verifyToken (token: "some-token") {
                        payload
                    }
                }"""
        response = self.client.post(self.url, data={'query': query})
        error_messages = [
            x['message'] for x in response.json()['errors'] if x is not None]
        self.assertNotIn(NOT_LOGGED_IN_MSG, error_messages)

    def test_query_with_expert(self):
        with self.login(email=self.basic_user().email):
            user = ExpertFactory()
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        user {{ firstName }}
                        bio
                        imageUrl
                        availableOfficeHours
                        officeHoursUrl
                        programInterests
                    }}
                }}
            """.format(id=user.id)
            response = self.client.post(self.url, data={'query': query})
            profile = user.expertprofile
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'user': {
                                'firstName': user.first_name,
                            },
                            'bio': profile.bio,
                            'imageUrl': (profile.image and
                                         profile.image.url or ''),
                            'availableOfficeHours': False,
                            'officeHoursUrl': None,
                            'programInterests': [],
                        }
                    }
                }
            )

    def test_query_with_entrepreneur(self):
        with self.login(email=self.staff_user().email):
            context = StartupTeamMemberContext(primary_contact=False)
            startup = context.startup
            program = context.program

            ApplicationFactory(cycle=context.cycle, startup=startup)
            ps = ProgramStartupStatusFactory(
                program=program,
                startup_list_tab_id='finalists')
            StartupStatusFactory(
                startup=startup,
                program_startup_status=ps
            )

            user = context.user
            profile = user.entrepreneurprofile
            member = context.member

            query = """
                query {{
                    entrepreneurProfile(id: {id}) {{
                        title
                        twitterHandle
                        imageUrl
                        linkedInUrl
                        facebookUrl
                        personalWebsiteUrl
                        phone
                        user {{
                            id
                            email
                            firstName
                            lastName
                        }}
                        startups {{
                            id
                            name
                            shortPitch
                            highResolutionLogo
                            program {{
                                year
                                family
                            }}
                        }}
                    }}
                }}
            """.format(id=user.id)
            response = self.client.post(self.url, data={'query': query})
            data = json.loads(response.content.decode("utf-8"))["data"]
            ent_profile = data["entrepreneurProfile"]

            self.assertEqual(ent_profile["title"], member.title)

            self.assertEqual(
                ent_profile["imageUrl"],
                profile.image.url if profile.image else "")
            self.assertEqual(
                ent_profile["linkedInUrl"], profile.linked_in_url)
            self.assertEqual(
                ent_profile["personalWebsiteUrl"],
                profile.personal_website_url)
            self.assertEqual(ent_profile["phone"], profile.phone)
            self.assertEqual(
                ent_profile["facebookUrl"], profile.facebook_url)
            self.assertEqual(
                ent_profile["twitterHandle"], profile.twitter_handle)

            user_resp = ent_profile["user"]
            self.assertEqual(user_resp["id"], str(user.id))
            self.assertEqual(user_resp["email"], user.email)
            self.assertEqual(user_resp["firstName"], user.first_name)
            self.assertEqual(user_resp["lastName"], user.last_name)

            startup_response = ent_profile["startups"][0]
            self.assertEqual(startup_response["id"], str(startup.id))
            self.assertEqual(startup_response["name"], startup.name)
            self.assertEqual(
                startup_response["shortPitch"], startup.short_pitch)
            self.assertEqual(
                startup_response["highResolutionLogo"],
                startup.high_resolution_logo.url
                if startup.high_resolution_logo else None)

            program_resp = startup_response["program"]
            self.assertEqual(
                program_resp["family"], str(program.program_family.name))
            self.assertEqual(
                program_resp["year"],
                str(program.start_date.year) if program.start_date else None)

    def test_office_url_field_returns_correct_value(self):
        program = ProgramFactory()
        confirmed = ExpertFactory()
        confirmed_role = UserRoleFactory(name=UserRole.MENTOR)
        program_role = ProgramRoleFactory(program=program,
                                          user_role=confirmed_role)

        program_grant_role = ProgramRoleGrantFactory(
            person=confirmed,
            program_role=program_role,
        )
        mentor_program = program_grant_role.program_role.program
        family_slug = mentor_program.program_family.url_slug
        program_slug = mentor_program.url_slug
        office_hours_url = (
                        "/officehours/list/{family_slug}/{program_slug}/"
                        .format(
                            family_slug=family_slug,
                            program_slug=program_slug) + (
                            '?mentor_id={mentor_id}'.format(
                                mentor_id=confirmed.id)))

        query = """
            query {{
                expertProfile(id: {id}) {{
                    user {{ firstName }}
                    officeHoursUrl
                }}
            }}
        """.format(id=confirmed.id)

        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'user': {
                                'firstName': confirmed.first_name,
                            },
                            'officeHoursUrl': office_hours_url
                        }
                    }
                }
            )

    def test_requested_fields_for_startup_mentor_relationship_type(self):
        with self.login(email=self.basic_user().email):
            mentor = ExpertFactory()
            relationship = StartupMentorRelationshipFactory(mentor=mentor)
            startup = relationship.startup_mentor_tracking.startup
            program = relationship.startup_mentor_tracking.program
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        currentMentees {{
                            {MENTEE_FIELDS}
                        }}
                        previousMentees {{
                            {MENTEE_FIELDS}
                        }}
                    }}
                }}
            """.format(id=relationship.mentor.id,
                       MENTEE_FIELDS=MENTEE_FIELDS)
            response = self.client.post(self.url, data={'query': query})
            self.assertEqual(
                json.loads(response.content.decode("utf-8")),
                {
                    'data': {
                        'expertProfile': {
                            'currentMentees': [{
                                'startup': {
                                    'id': str(startup.id),
                                    'name': startup.name,
                                    'highResolutionLogo':
                                        (startup.high_resolution_logo and
                                            startup.high_resolution_logo.url or
                                            None),
                                    'shortPitch': startup.short_pitch,
                                },
                                'program': {
                                        'family':
                                            program.program_family.name,
                                        'year': str(program.start_date.year),
                                },
                            }],
                            'previousMentees': []
                        }
                    }
                }
            )

    def test_query_with_non_expert_user_id(self):
        with self.login(email=self.basic_user().email):
            user = EntrepreneurFactory()
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        user {{ firstName }}
                        bio
                    }}
                }}
            """.format(id=user.id)

            with capture_stderr(self.client.post,
                                self.url,
                                data={'query': query}) as (response, _):
                error_messages = [x['message'] for x in
                                  response.json()['errors']]

            self.assertIn(EXPERT_NOT_FOUND_MESSAGE, error_messages)
            self.assertEqual(
                response.json()['data']['expertProfile'],
                None
            )

    def test_query_with_non_existent_entrepreneur_id(self):
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    entrepreneurProfile(id: {id}) {{
                        user {{ firstName }}
                    }}
                }}
            """.format(id=0)

            with capture_stderr(self.client.post,
                                self.url,
                                data={'query': query}) as (response, _):
                error_messages = [x['message'] for x in
                                  response.json()['errors']]

            self.assertIn(ENTREPRENEUR_NOT_FOUND_MESSAGE, error_messages)
            self.assertEqual(
                response.json()['data']['entrepreneurProfile'],
                None
            )

    def test_non_staff_user_cannot_access_non_finalist_graphql_view(self):
        query_string = "query {{ entrepreneurProfile(id: {id}) {{ title }} }}"
        with self.login(email=self.basic_user().email):
            user = EntrepreneurFactory()
            query = query_string.format(id=user.id)

            with capture_stderr(self.client.post,
                                self.url,
                                data={'query': query}) as (response, _):
                error_messages = [x['message']
                                  for x in response.json()['errors']]

            self.assertIn(NON_FINALIST_PROFILE_MESSAGE, error_messages)

    def test_staff_user_can_access_non_finalist_graphql_view(self):
        with self.login(email=self.staff_user().email):
            user = EntrepreneurFactory()
            query = """
                        query {{
                                entrepreneurProfile(id: {id}) {{
                                    user {{ firstName }}
                                }}
                            }}
                    """.format(id=user.id)
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'entrepreneurProfile': {
                            'user': {
                                'firstName': user.first_name
                            },
                        }
                    }
                }
            )

    def test_non_staff_user_can_access_finalist_graphql_view(self):
        with self.login(email=self.basic_user().email):
            user = EntrepreneurFactory()
            UserRoleContext(UserRole.FINALIST, user=user)
            query = """
                        query {{
                                entrepreneurProfile(id: {id}) {{
                                    user {{ firstName }}
                                }}
                            }}
                    """.format(id=user.id)
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'entrepreneurProfile': {
                            'user': {
                                'firstName': user.first_name
                            },
                        }
                    }
                }
            )

    def test_query_program_roles_for_entrepreneur_returns_correct_value(self):
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        user = UserContext(
            program_role_names=user_roles_of_interest).user

        program_roles = get_user_program_and_startup_roles(
            user,
            user_roles_of_interest)
        query = """
            query{{
                entrepreneurProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)
        expected_json = {
                    'data': {
                        'entrepreneurProfile': {
                            'programRoles': program_roles
                        }
                    }
                }
        self._assert_response_equals_json(query, expected_json)

    def test_query_program_roles_for_expert_returns_correct_value(self):
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        user = UserContext(
            user_type="EXPERT",
            program_role_names=user_roles_of_interest).user

        program_roles = get_user_program_and_startup_roles(
            user,
            user_roles_of_interest)

        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)
        expected_json = {
                    'data': {
                        'expertProfile': {
                            'programRoles': program_roles
                        }
                    }
                }
        self._assert_response_equals_json(query, expected_json)

    def test_query_program_roles_program_role_names_are_normalized(self):
        program_role_name = "BEST IN SHOW (BOS)"
        user_role_name = UserRole.FINALIST
        user = ExpertFactory()
        ProgramRoleGrantFactory(
            person=user,
            program_role__name=program_role_name,
            program_role__user_role__name=user_role_name)
        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})

        normalized_role_name = program_role_name.title().split(" (")[0]
        response_dict = json.loads(response.content)
        program_roles = response_dict['data']['expertProfile']['programRoles']
        self.assertIn([normalized_role_name], program_roles.values())

    def test_query_program_roles_for_expert_with_same_program(self):
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        user = UserContext(
            user_type="EXPERT",
            program_role_names=user_roles_of_interest).user
        program_roles = get_user_program_and_startup_roles(
            user,
            user_roles_of_interest)

        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)
        expected_json = {
                    'data': {
                        'expertProfile': {
                            'programRoles': program_roles
                        }
                    }
                }
        self._assert_response_equals_json(query, expected_json)

    def test_query_prg_roles_for_selected_roles(self):
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        startup_roles_of_interest = [StartupRole.ENTRANT]
        startup_status_names = [StartupRole.ENTRANT,
                                StartupRole.FINALIST,
                                StartupRole.FINALIST,
                                StartupRole.ENTRANT]
        user = UserContext(
            user_type="EXPERT",
            program_role_names=user_roles_of_interest,
            startup_status_names=startup_status_names).user
        program_roles = get_user_program_and_startup_roles(
            user, user_roles_of_interest, startup_roles_of_interest)

        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)
        expected_json = {
            'data': {
                'expertProfile': {
                    'programRoles': program_roles
                }
            }
        }

        self._assert_response_equals_json(query, expected_json)

    def test_get_user_confirmed_mentor_program_families(self):
        role_grant = ProgramRoleGrantFactory(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS,
            program_role__user_role__name=UserRole.MENTOR,
            person=ExpertFactory(),
        )
        user = role_grant.person
        user_program = role_grant.program_role.program
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        confirmedMentorProgramFamilies
                    }}
                }}
            """.format(id=user.id)

            response = self.client.post(self.url, data={'query': query})
            data = json.loads(response.content.decode("utf-8"))["data"]
            expert_profile = data["expertProfile"]

            self.assertEqual(
                expert_profile["confirmedMentorProgramFamilies"],
                [user_program.program_family.name])

    def test_query_for_user_without_confirmed_mentor_program_families(self):
        user = ExpertFactory()
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        confirmedMentorProgramFamilies
                    }}
                }}
            """.format(id=user.id)

            response = self.client.post(self.url, data={'query': query})
            data = json.loads(response.content.decode("utf-8"))["data"]
            expert_profile = data["expertProfile"]
            self.assertEqual(expert_profile["confirmedMentorProgramFamilies"],
                             [])

    def _assert_response_equals_json(self, query, expected_json):
        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                expected_json
            )
