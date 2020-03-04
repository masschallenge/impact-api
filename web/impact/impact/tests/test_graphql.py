# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import json
from django.urls import reverse

from accelerator.models import (
    UserRole, StartupRole
)
from impact.graphql.middleware import NOT_LOGGED_IN_MSG
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import (
    EntrepreneurFactory,
    ExpertFactory,
    ProgramFactory,
    ProgramRoleGrantFactory,
    ProgramRoleFactory,
    StartupMentorRelationshipFactory,
    UserRoleFactory,
    StartupRoleFactory,
    ApplicationFactory,
    ProgramStartupStatusFactory,
    StartupStatusFactory,
    StartupFactory,
)
from impact.tests.utils import capture_stderr
from impact.graphql.query import (
    EXPERT_NOT_FOUND_MESSAGE,
    ENTREPRENEUR_NOT_FOUND_MESSAGE,
    NON_FINALIST_PROFILE_MESSAGE
)
from accelerator.tests.contexts import StartupTeamMemberContext, UserRoleContext

from impact.utils import (
    get_user_startup_prg_role_by_program_family, combine_prg_roles,
    get_user_prg_role_by_program_family
)

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
        with self.login(email=self.basic_user().email):
            user = EntrepreneurFactory()
            query = """query {{ entrepreneurProfile(id: {id}) {{ title }} }}""".format(id=user.id)

            with capture_stderr(self.client.post,
                                self.url,
                                data={'query': query}) as (response, _):
                error_messages = [x['message'] for x in response.json()['errors']]

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
        # prepare user program roles
        program = ProgramFactory()
        alum_role = UserRoleFactory(name=UserRole.ALUM)
        finalist_role = UserRoleFactory(name=UserRole.FINALIST)
        alum_program_role = ProgramRoleFactory(program=program,
                                                user_role=alum_role)
        finalist_program_role = ProgramRoleFactory(program=program,
                                                    user_role=finalist_role)
        user = EntrepreneurFactory()
        ProgramRoleGrantFactory( person=user,program_role=alum_program_role)
        ProgramRoleGrantFactory(person=user,program_role=finalist_program_role)

        user_prg_roles = get_user_prg_role_by_program_family(
           user, [UserRole.FINALIST, UserRole.ALUM]
        )

        # prepare startup program role
        startup = StartupFactory(user=user)
        program_startup_status = ProgramStartupStatusFactory(
            startup_role=StartupRoleFactory(name=StartupRole.ENTRANT),
            program = ProgramFactory()
        )
        startup_status = StartupStatusFactory(
            startup=startup,
            program_startup_status=program_startup_status
        )

        startup_pgr_roles = get_user_startup_prg_role_by_program_family(
            user
        )
        program_roles = combine_prg_roles(user_prg_roles, startup_pgr_roles)
        query = """
            query{{
                entrepreneurProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)

        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'entrepreneurProfile': {
                            'programRoles': program_roles
                        }
                    }
                }
            )

    def test_query_program_roles_for_expert_returns_correct_value(self):

        # prepare user program role
        program = ProgramFactory()
        alum_role = UserRoleFactory(name=UserRole.ALUM)
        finalist_role = UserRoleFactory(name=UserRole.FINALIST)
        alum_program_role = ProgramRoleFactory(program=program,
                                                user_role=alum_role)
        finalist_program_role = ProgramRoleFactory(program=program,
                                                    user_role=finalist_role)
        user = ExpertFactory()
        ProgramRoleGrantFactory(person=user,program_role=alum_program_role)
        ProgramRoleGrantFactory( person=user,program_role=finalist_program_role)

        user_prg_roles = get_user_prg_role_by_program_family(
           user, [UserRole.FINALIST, UserRole.ALUM]
        )

        # prepare startup program role
        startup = StartupFactory(user=user)
        program_startup_status = ProgramStartupStatusFactory(
            startup_role=StartupRoleFactory(name=StartupRole.ENTRANT),
            program = ProgramFactory()
        )
        startup_status = StartupStatusFactory(
            startup=startup,
            program_startup_status=program_startup_status
        )

        startup_pgr_roles = get_user_startup_prg_role_by_program_family(
            user
        )
        program_roles = combine_prg_roles(user_prg_roles, startup_pgr_roles)


        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)

        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'programRoles': program_roles
                        }
                    }
                }
            )

    def test_query_program_roles_for_expert_with_same_program(self):

        # prepare user program role
        program = ProgramFactory()
        alum_role = UserRoleFactory(name=UserRole.ALUM)
        finalist_role = UserRoleFactory(name=UserRole.FINALIST)
        alum_program_role = ProgramRoleFactory(program=program,
                                                user_role=alum_role)
        finalist_program_role = ProgramRoleFactory(program=program,
                                                    user_role=finalist_role)
        user = ExpertFactory()
        ProgramRoleGrantFactory(person=user,program_role=alum_program_role)
        ProgramRoleGrantFactory( person=user,program_role=finalist_program_role)

        user_prg_roles = get_user_prg_role_by_program_family(
           user, [UserRole.FINALIST, UserRole.ALUM]
        )

        # prepare startup program role
        startup = StartupFactory(user=user)
        program_startup_status = ProgramStartupStatusFactory(
            startup_role=StartupRoleFactory(name=StartupRole.ENTRANT),
            program = program
        )
        startup_status = StartupStatusFactory(
            startup=startup,
            program_startup_status=program_startup_status
        )

        startup_pgr_roles = get_user_startup_prg_role_by_program_family(
            user
        )
        program_roles = combine_prg_roles(user_prg_roles, startup_pgr_roles)


        query = """
            query{{
                expertProfile(id:{id}) {{
                    programRoles
                }}
            }}
        """.format(id=user.id)

        with self.login(email=self.basic_user().email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'programRoless': program_roles
                        }
                    }
                }
            )
