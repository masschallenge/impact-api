# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import time

from algoliasearch import algoliasearch
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accelerator.models import UserRole
from accelerator_abstract.models import CURRENT_STATUSES


class AlgoliaApiKeyView(APIView):
    view_name = 'algolia_api_key_view'

    permission_classes = (
        permissions.IsAuthenticated,
    )

    actions = ["GET"]

    def get(self, request, format=None):
        search_key = _get_search_key(request)
        filters = _get_filters(request)
        params = {
            'hitsPerPage': 24,
            'validUntil': int(time.time()) + 3600,
            'userToken': request.user.id,
            'filters': filters
        }
        public_key = _get_public_key(params, search_key)
        return Response({
            'token': public_key,
            'index_prefix': settings.ALGOLIA_INDEX_PREFIX,
            'filters': filters
        })


def _get_search_key(request):
    if request.user.is_staff:
        return settings.ALGOLIA_STAFF_SEARCH_ONLY_API_KEY
    return settings.ALGOLIA_SEARCH_ONLY_API_KEY


def _get_filters(request):
    if request.user.is_staff:
        return []
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
        return " OR ".join(facet_filters)
    else:
        return "is_confirmed_mentor:true"


def _get_public_key(params, search_key):
    client = algoliasearch.Client(
        settings.ALGOLIA_APPLICATION_ID,
        settings.ALGOLIA_API_KEY)
    public_key = client.generateSecuredApiKey(search_key, params)
    return public_key
