# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from django.urls import reverse

from accelerator.models import (
    UserRole,
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
)
from impact.tests.utils import capture_stderr

MENTEE_FIELDS = """
    startupId
    startupName
    startupHighResolutionLogo
    startupShortPitch
    programLocation
    programYear
    programStatus
"""

EXPERT_NOT_FOUND_MESSAGE = 'ExpertProfile matching query does not exist.'


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
        error_messages = [x['message'] for x in response.json()['errors']]
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
                            'programInterests': []
                        }
                    }
                }
            )

    def test_office_url_field_returns_correct_value(self):
        program = ProgramFactory()
        confirmed = ExpertFactory()
        confirmed_role = UserRoleFactory(name=UserRole.MENTOR)
        program_role = ProgramRoleFactory(program=program,
                                          user_role=confirmed_role)
        program_grant_role = ProgramRoleGrantFactory(
            person=confirmed,
            program_role=program_role)
        mentor_profile = confirmed.get_profile()
        mentor_program = program_grant_role.program_role.program
        family_slug = mentor_program.program_family.url_slug
        program_slug = mentor_program.url_slug
        office_hours_url = ("/officehours/{family_slug}/{program_slug}/"
                            .format(
                                family_slug=family_slug,
                                program_slug=program_slug) + (
                                '?mentor_id={mentor_id}'.format(
                                    mentor_id=mentor_profile.user_id)))

        query = """
            query {{
                expertProfile(id: {id}) {{
                    user {{ firstName }}
                    officeHoursUrl
                }}
            }}
        """.format(id=mentor_profile.user_id)

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
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'currentMentees': [{
                                'startupId': str(startup.id),
                                'startupName': startup.name,
                                'startupHighResolutionLogo':
                                    (startup.high_resolution_logo and
                                     startup.high_resolution_logo.url or
                                     ''),
                                'startupShortPitch': startup.short_pitch,
                                'programLocation':
                                    program.program_family.name,
                                'programYear': str(program.start_date.year),
                                'programStatus': program.program_status
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

    def test_query_with_non_existent_user_id(self):
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        user {{ firstName }}
                    }}
                }}
            """.format(id=0)

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
