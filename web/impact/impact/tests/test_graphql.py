# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import json
from django.urls import reverse

from accelerator.models import StartupRole, UserRole
from accelerator.tests.contexts import (
    StartupTeamMemberContext,
    UserRoleContext
)
from accelerator.tests.contexts.context_utils import get_user_role_by_name
from accelerator.models import (
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS
)
from impact.graphql.middleware import NOT_LOGGED_IN_MSG
from impact.graphql.query import (
    ENTREPRENEUR_NOT_FOUND_MESSAGE,
    EXPERT_NOT_FOUND_MESSAGE,
    NOT_ALLOWED_ACCESS_MESSAGE
)
from impact.tests.api_test_case import APITestCase
from impact.tests.contexts import UserContext
from impact.tests.factories import (
    ApplicationFactory,
    EntrepreneurFactory,
    ExpertFactory,
    ProgramFactory,
    ProgramRoleFactory,
    ProgramRoleGrantFactory,
    ProgramStartupStatusFactory,
    StartupMentorRelationshipFactory,
    ProgramFamilyLocationFactory,
    StartupStatusFactory,
    ProgramFamilyFactory,
    UserRoleFactory,
    LocationFactory,
)
from impact.tests.utils import capture_stderr
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

MENTOR_PRG_QUERY = """
            query {{
                expertProfile(id: {id}){{
                    mentorProgramRoleGrants
                }}
            }}
        """


class TestGraphQL(APITestCase):
    url = reverse('graphql')
    auth_url = reverse('graphql-auth')

    def test_anonymous_user_cannot_access_main_graphql_view(self):
        user = ExpertFactory()
        query = """query {{ expertProfile(id: {id}) {{ title }} }}
            """.format(id=user.id)
        self._assert_error_in_response(query, NOT_LOGGED_IN_MSG)

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
                    mentorProgramRoleGrants
                }}
            }}
        """.format(id=user.id)
        profile = user.expertprofile
        expected_json = {
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
                    'mentorProgramRoleGrants': {'results': []}
                }
            }
        }
        self._assert_response_equals_json(query, expected_json)

    def test_mentor_program_role_grants(self):
        user = ExpertFactory()
        role_grant = ProgramRoleGrantFactory.create(
            program_role__user_role__name=UserRole.MENTOR,
            person=user)
        program = role_grant.program_role.program
        program_overview_link = program.program_overview_link

        query = MENTOR_PRG_QUERY.format(id=user.id)

        expected_json = {
            'data': {
                'expertProfile': {
                    'mentorProgramRoleGrants': {'results': [
                        {'id': role_grant.id,
                         'program_end_date': program.end_date.isoformat(),
                         'program_id': program.id,
                         'program_name': program.name,
                         'program_overview_link': program_overview_link,
                         'program_start_date': program.start_date.isoformat(),
                         'user_role_name': UserRole.MENTOR
                         }]
                    }
                }
            }}
        self._assert_response_equals_json(query, expected_json)

    def test_mentor_program_role_grants_only_returns_mentor_roles(self):
        user = ExpertFactory()
        program = ProgramFactory()
        mentor_role_grant = ProgramRoleGrantFactory.create(
            program_role__user_role__name=UserRole.MENTOR, person=user)
        program = mentor_role_grant.program_role.program
        program_overview_link = program.program_overview_link
        ProgramRoleGrantFactory.create(
            program_role__user_role__name=UserRole.JUDGE, person=user)

        query = MENTOR_PRG_QUERY.format(id=user.id)

        expected_json = {
            'data': {
                'expertProfile': {
                    'mentorProgramRoleGrants': {'results': [
                        {'id': mentor_role_grant.id,
                         'program_end_date': program.end_date.isoformat(),
                         'program_id': program.id,
                         'program_name': program.name,
                         'program_overview_link': program_overview_link,
                         'program_start_date': program.start_date.isoformat(),
                         'user_role_name': UserRole.MENTOR
                         }]
                    }
                }
            }}
        self._assert_response_equals_json(query, expected_json)

    def test_query_with_entrepreneur(self):
        with self.login(email=self.staff_user().email):
            context = StartupTeamMemberContext(primary_contact=False)
            startup = context.startup
            program = context.program

            ApplicationFactory(cycle=context.cycle, startup=startup)
            ps = ProgramStartupStatusFactory(
                startup_status=StartupRole.GOLD_WINNER,
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
                            programStartupStatus
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
                startup_response["programStartupStatus"],
                [StartupRole.GOLD_WINNER])
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

        expected_json = {
            'data': {
                'expertProfile': {
                    'user': {
                        'firstName': confirmed.first_name,
                    },
                    'officeHoursUrl': office_hours_url
                }
            }
        }

        self._assert_response_equals_json(query, expected_json)

    def test_requested_fields_for_startup_mentor_relationship_type(self):
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
        expected_json = {
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
        self._assert_response_equals_json(query, expected_json)

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

            self._assert_error_in_response(query, EXPERT_NOT_FOUND_MESSAGE)

    def test_query_with_non_existent_entrepreneur_id(self):
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    entrepreneurProfile(id: {id}) {{
                        user {{ firstName }}
                    }}
                }}
            """.format(id=0)

            self._assert_error_in_response(
                query, ENTREPRENEUR_NOT_FOUND_MESSAGE)

    def test_non_staff_user_cannot_access_non_finalist_graphql_view(self):
        query_string = "query {{ entrepreneurProfile(id: {id}) {{ title }} }}"
        with self.login(email=self.basic_user().email):
            user = EntrepreneurFactory()
            query = query_string.format(id=user.id)

            self._assert_error_in_response(query, NOT_ALLOWED_ACCESS_MESSAGE)

    def test_staff_user_can_access_non_finalist_graphql_view(self):
        user = EntrepreneurFactory()
        query = """
                    query {{
                            entrepreneurProfile(id: {id}) {{
                                user {{ firstName }}
                            }}
                        }}
                """.format(id=user.id)
        expected_json = {
            'data': {
                'entrepreneurProfile': {
                    'user': {
                        'firstName': user.first_name
                    },
                }
            }
        }
        self._assert_response_equals_json(query, expected_json, True)

    def test_non_staff_user_can_access_finalist_graphql_view(self):
        current_user = expert_user(UserRole.MENTOR)
        user = EntrepreneurFactory()
        UserRoleContext(UserRole.FINALIST, user=user)
        query = """
            query {{
                entrepreneurProfile(id: {id}) {{
                    user {{ firstName }}
                }}
            }}
        """.format(id=user.id)
        expected_json = {
            'data': {
                'entrepreneurProfile': {
                    'user': {
                        'firstName': user.first_name
                    },
                }
            }
        }
        self._assert_response_equals_json(
            query, expected_json, email=current_user.email)

    def test_query_program_roles_for_entrepreneur_returns_correct_value(self):
        current_user = expert_user(UserRole.AIR)
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
        self._assert_response_equals_json(
            query, expected_json, email=current_user.email)

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

    def test_query_for_prg_roles_as_staff_user(self):
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
        self._assert_response_equals_json(query, expected_json, True)

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

    def test_user_can_view_profile_with_non_current_allowed_roles(self):
        allowed_user = expert_user(UserRole.FINALIST)
        user = EntrepreneurFactory()
        UserRoleContext(
            UserRole.MENTOR,
            user=user,
            program=ProgramFactory(program_status=ENDED_PROGRAM_STATUS))
        query = """
                    query{{
                        entrepreneurProfile(id:{id}) {{
                            programRoles
                        }}
                    }}
                """.format(id=user.id)

        expected_json={'data': {'entrepreneurProfile': {'programRoles': {}}}}
        self._assert_response_equals_json(
            query, expected_json, email=allowed_user.email)

    def test_allowed_user_with_non_current_user_role_cannot_view_profile(self):
        current_user = expert_user(
            UserRole.FINALIST,
            program_status=ENDED_PROGRAM_STATUS)
        with self.login(email=current_user.email):
            user = EntrepreneurFactory()
            UserRoleContext(UserRole.MENTOR, user=user)
            query = """
                        query{{
                            entrepreneurProfile(id:{id}) {{
                                user{{lastName}}
                            }}
                        }}
                    """.format(id=user.id)
            self._assert_error_in_response(query, NOT_ALLOWED_ACCESS_MESSAGE)

    def test_current_finalist_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.FINALIST,
                                             UserRole.FINALIST)

    def test_current_finalist_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.FINALIST, UserRole.STAFF)

    def test_current_finalist_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.FINALIST, UserRole.ALUM)

    def test_current_finalist_can_view_current_mentor_profile(self):
        self._assert_expert_can_view_profile(UserRole.FINALIST,
                                             UserRole.MENTOR)

    def test_current_alum_in_residence_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.AIR, UserRole.FINALIST)

    def test_current_alum_in_residence_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.AIR, UserRole.STAFF)

    def test_current_alum_in_residence_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.AIR, UserRole.ALUM)

    def test_current_alum_in_residence_can_view_current_mentor_profile(self):
        self._assert_expert_can_view_profile(UserRole.AIR, UserRole.MENTOR)

    def test_current_mentor_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.MENTOR,
                                             UserRole.FINALIST)

    def test_current_mentor_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.MENTOR, UserRole.STAFF)

    def test_current_mentor_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.MENTOR, UserRole.ALUM)

    def test_current_mentor_can_view_current_mentor_profile(self):
        self._assert_expert_can_view_profile(UserRole.MENTOR, UserRole.MENTOR)

    def test_current_partner_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.PARTNER,
                                             UserRole.FINALIST)

    def test_current_partner_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.PARTNER, UserRole.STAFF)

    def test_current_partner_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.PARTNER, UserRole.ALUM)

    def test_current_partner_can_view_current_mentor_profile(self):
        self._assert_expert_can_view_profile(UserRole.PARTNER, UserRole.MENTOR)

    def test_current_alum_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.ALUM, UserRole.FINALIST)

    def test_current_alum_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.ALUM, UserRole.STAFF)

    def test_current_alum_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.ALUM, UserRole.ALUM)

    def test_current_alum_can_view_current_mentor_profile(self):
        self._assert_expert_can_view_profile(UserRole.ALUM, UserRole.MENTOR)

    def test_current_judge_can_view_current_finalist_profile(self):
        self._assert_expert_can_view_profile(UserRole.JUDGE, UserRole.FINALIST)

    def test_current_judge_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(UserRole.JUDGE, UserRole.STAFF)

    def test_current_judge_can_view_current_alum_profile(self):
        self._assert_expert_can_view_profile(UserRole.JUDGE, UserRole.ALUM)

    def test_user_with_no_role_can_view_current_staff_profile(self):
        self._assert_expert_can_view_profile(None, UserRole.STAFF)

    def test_user_with_no_role_cannot_view_current_finalist_profile(self):
        self._assert_expert_cannot_view_profile(None, UserRole.FINALIST)

    def test_user_with_no_role_can_view_current_alum_profile(self):
        self._assert_expert_cannot_view_profile(None, UserRole.ALUM)

    def test_user_with_no_role_can_view_current_mentor_profile(self):
        self._assert_expert_cannot_view_profile(None, UserRole.MENTOR)

    def test_current_judge_cannot_view_mentor_profile(self):
        self._assert_expert_cannot_view_profile(UserRole.JUDGE,
                                                UserRole.MENTOR)

    def test_loggedin_expert_data_is_returned_on_missing_id(self):
        user = expert_user(UserRole.MENTOR)

        query, expected_json = _user_query(user, "expertProfile")
        self._assert_response_equals_json(
            query, expected_json, email=user.email)

    def test_logged_in_entrepreneur_data_is_returned_on_missing_id(self):
        user = EntrepreneurFactory()
        user_role = get_user_role_by_name(UserRole.FINALIST)
        program_role = ProgramRoleFactory.create(
            user_role=user_role,
            program__program_status=ACTIVE_PROGRAM_STATUS
        )
        ProgramRoleGrantFactory(person=user,
                                program_role=program_role)
        user.set_password('password')
        user.save()

        query, expected_json = _user_query(user, "entrepreneurProfile")
        self._assert_response_equals_json(
            query, expected_json, email=user.email)

    def test_assert_office_hour_location_is_returned(self):

        program_family = ProgramFamilyFactory()
        desired_user_roles = [
            UserRole.MENTOR, UserRole.FINALIST, UserRole.AIR]

        user = UserContext(
            user_type='EXPERT',
            program_role_names=desired_user_roles,
            program_families=[program_family]
        ).user

        program_role = user.programrolegrant_set.filter(
            program_role__program__program_status="active",
            program_role__user_role__name__in=desired_user_roles
        ).first().program_role

        program_family = program_role.program.program_family

        location = LocationFactory(
            name='Nigeria', street_address='18 pius eze', city='Ago')

        location1 = LocationFactory(
            name='Remote', street_address='18 pius eze', city='Ago')

        ProgramFamilyLocationFactory.create(
            program_family=program_family, location=location)

        ProgramFamilyLocationFactory.create(
            program_family=program_family, location=location1)

        query = """
            query{{
                expertProfile(id:{id})  {{
                    officeHourLocations{{name}}
                }}
            }}
        """.format(id=user.id)

        expected_json = {
            'data': {
                'expertProfile': {
                    'officeHourLocations': [
                        {
                            'name': location.name
                        },
                        {
                            'name': 'Remote'
                        }
                    ]
                }
            }
        }

        self._assert_response_equals_json(
            query=query, expected_json=expected_json)

    def _assert_expert_can_view_profile(self, expert_role, profile_user_role):
        current_user = expert_user(expert_role)
        user = EntrepreneurFactory()
        UserRoleContext(profile_user_role, user=user)
        query = """
            query{{
                entrepreneurProfile(id:{id}) {{
                    user{{lastName}}
                }}
            }}
        """.format(id=user.id)
        expected_json = {
            'data': {
                'entrepreneurProfile': {
                    'user': {
                        'lastName': user.last_name
                    }
                }
            }
        }
        self._assert_response_equals_json(
            query, expected_json, email=current_user.email)

    def _assert_expert_cannot_view_profile(self, user_role, profile_user_role):
        current_user = expert_user(user_role)
        with self.login(email=current_user.email):
            user = EntrepreneurFactory()
            UserRoleContext(profile_user_role, user=user)
            query = """
                        query{{
                        entrepreneurProfile(id:{id}) {{
                            programRoles
                        }}
                    }}
                    """.format(id=user.id)
            self._assert_error_in_response(query, NOT_ALLOWED_ACCESS_MESSAGE)

    def _assert_response_equals_json(
            self,
            query,
            expected_json,
            is_staff=False,
            email=None):
        if is_staff:
            user = self.staff_user()
        else:
            user = self.basic_user()
        with self.login(email=email or user.email):
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                expected_json
            )

    def _assert_error_in_response(self, query, error_message):
        with capture_stderr(self.client.post,
                            self.url,
                            data={'query': query}) as (response, _):
            error_messages = [x['message']
                              for x in response.json()['errors']]
        self.assertIn(error_message, error_messages)


def expert_user(role=None, program_status=None):
    user = ExpertFactory()
    if role:
        user_role = get_user_role_by_name(role)
        program_role = ProgramRoleFactory.create(
            user_role=user_role,
            program__program_status=program_status or ACTIVE_PROGRAM_STATUS
        )
        ProgramRoleGrantFactory(person=user,
                                program_role=program_role)
    user.set_password('password')
    user.save()
    return user


def _user_query(user, profile):
    query = """
            query{{
                {profile} {{
                    user{{lastName}}
                }}
            }}
        """.format(profile=profile)
    expected_json = {}
    expected_json["data"] = {}
    expected_json["data"][profile] = {
        'user': {
            'lastName': user.last_name
        }
    }
    return query, expected_json
