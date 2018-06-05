# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from algoliasearch import algoliasearch
from django.conf import settings
from accelerator_abstract.models import CURRENT_STATUSES
from accelerator.models import UserRole
import time


class AlgoliaApiKeyView(APIView):
    view_name = 'algolia_api_key_view'

    permission_classes = (
        permissions.IsAuthenticated,
    )

    actions = ["GET"]

    def get(self, request, format=None):
        index_prefix = settings.ALGOLIA_INDEX_PREFIX
        client = algoliasearch.Client(
            settings.ALGOLIA_APPLICATION_ID,
            settings.ALGOLIA_API_KEY)
        params = {
            'hitsPerPage': 24,
            'validUntil': int(time.time()) + 3600,
            'userToken': request.user.id
        }
        search_key = settings.ALGOLIA_SEARCH_ONLY_API_KEY
        if request.user.is_staff:
            search_key = settings.ALGOLIA_STAFF_SEARCH_ONLY_API_KEY
        else:
            active_roles = UserRole.FINALIST_USER_ROLES
            active_roles.append(UserRole.MENTOR)
            facet_filters = []
            for grant in request.user.programrolegrant_set.filter(
                    program_role__program__program_status__in=CURRENT_STATUSES,
                    program_role__user_role__name__in=active_roles
            ):
                facet_filters.append(
                    'confirmed_mentor_programs:"{active_program}"'.format(
                        active_program=grant.program_role.program.name))
            if len(facet_filters) > 0:
                params['filters'] = " OR ".join(facet_filters)
            else:
                params['filters'] = "is_confirmed_mentor:true"
        public_key = client.generateSecuredApiKey(
            search_key,
            params)

        return Response({
            'token': public_key,
            'index_prefix': index_prefix,
            'filters': params.get('filters', [])})
