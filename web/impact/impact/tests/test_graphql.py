# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
import json
from django.urls import reverse

from impact.graphql.middleware import NOT_LOGGED_IN_MSG
from impact.tests.api_test_case import APITestCase
from impact.tests.factories import (
    EntrepreneurFactory,
    ExpertFactory,
    StartupMentorRelationshipFactory,
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
                    }}
                }}
            """.format(id=user.id)
            response = self.client.post(self.url, data={'query': query})
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {
                    'data': {
                        'expertProfile': {
                            'user': {
                                'firstName': user.first_name,
                            },
                            'bio': user.expertprofile.bio,
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
                                    str(startup.high_resolution_logo),
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
            response = self.client.post(self.url, data={'query': query})
            response_payload = json.loads(response.content)
            self.assertEqual(
                response_payload['errors'][0]['message'],
                EXPERT_NOT_FOUND_MESSAGE
            )
            self.assertEqual(
                response_payload['data']['expertProfile'],
                None
            )

    def test_query_with_non_existant_user_id(self):
        with self.login(email=self.basic_user().email):
            query = """
                query {{
                    expertProfile(id: {id}) {{
                        user {{ firstName }}
                    }}
                }}
            """.format(id=0)
            response = self.client.post(self.url, data={'query': query})
            response_payload = json.loads(response.content)
            self.assertEqual(
                response_payload['errors'][0]['message'],
                EXPERT_NOT_FOUND_MESSAGE
            )
            self.assertEqual(
                response_payload['data']['expertProfile'],
                None
            )
