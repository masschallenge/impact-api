# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import time

from algoliasearch import algoliasearch
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accelerator.models import (
    Program,
    ProgramFamily,
    ProgramRole,
    UserRole,
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS,
)

IS_CONFIRMED_MENTOR_FILTER = "is_confirmed_mentor:true"
CONFIRMED_MENTOR_IN_PROGRAM_FILTER = 'confirmed_mentor_programs:"{program}"'


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
        }
        if filters:
            params['filters'] = filters
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
    participant_roles = UserRole.FINALIST_USER_ROLES
    participant_roles.append(UserRole.MENTOR)
    user_program_roles_as_participant = ProgramRole.objects.filter(
        programrolegrant__person=request.user,
        user_role__name__in=participant_roles
    )
    program_groups = Program.objects.filter(
        programrole__in=user_program_roles_as_participant).values_list(
        'mentor_program_group', flat=True).distinct()
    program_families = ProgramFamily.objects.filter(
        programs__mentor_program_group__in=program_groups).prefetch_related(
        'programs').distinct()
    facet_filters = _facet_filters(program_families)
    if len(facet_filters) > 0:
        return " OR ".join(facet_filters)
    else:
        return IS_CONFIRMED_MENTOR_FILTER


def _facet_filters(program_families):
    facet_filters = []
    for program_family in program_families:
        past_or_present_programs = program_family.programs.filter(
            program_status__in=(ACTIVE_PROGRAM_STATUS, ENDED_PROGRAM_STATUS)
        ).order_by('-start_date')
        if past_or_present_programs:
            facet_filters.append(CONFIRMED_MENTOR_IN_PROGRAM_FILTER.format(
                program=past_or_present_programs.first().name))
    return facet_filters


def _get_public_key(params, search_key):
    client = algoliasearch.Client(
        settings.ALGOLIA_APPLICATION_ID,
        settings.ALGOLIA_API_KEY)
    public_key = client.generateSecuredApiKey(search_key, params)
    return public_key
