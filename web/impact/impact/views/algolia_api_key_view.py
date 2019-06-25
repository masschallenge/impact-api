# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import time

from algoliasearch import algoliasearch
from django.conf import settings
from django.core.exceptions import PermissionDenied

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accelerator.models import (
    Program,
    ProgramFamily,
    ProgramRole,
    ProgramRoleGrant,
    UserRole,
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS,
)

from accelerator_abstract.models.base_user_utils import (
    is_entrepreneur,
    is_employee,
)

from accelerator_abstract.models.base_permission_checks import (
    base_accelerator_check
)

from impact.permissions import DirectoryAccessPermissions

IS_CONFIRMED_MENTOR_FILTER = "is_confirmed_mentor:true"
CONFIRMED_MENTOR_IN_PROGRAM_FILTER = 'confirmed_mentor_programs:"{program}"'
IS_TEAM_MEMBER_FILTER = 'is_team_member:true'
HAS_FINALIST_ROLE_FILTER = 'has_a_finalist_role:true'
IS_ACTIVE_FILTER = 'is_active:true'


class AlgoliaApiKeyView(APIView):
    view_name = 'algolia_api_key_view'

    permission_classes = (
        permissions.IsAuthenticated,
        DirectoryAccessPermissions,
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
    if is_employee(request.user):
        return settings.ALGOLIA_STAFF_SEARCH_ONLY_API_KEY
    return settings.ALGOLIA_SEARCH_ONLY_API_KEY


def _get_filters(request):
    if is_employee(request.user):
        return []


    if request.GET['index'] == 'people':
        if not base_accelerator_check(request.user):
            raise PermissionDenied()
        return _build_filter(
            IS_TEAM_MEMBER_FILTER,
            HAS_FINALIST_ROLE_FILTER, IS_ACTIVE_FILTER)


    if request.GET['index'] == 'mentor':
        participant_roles = [UserRole.AIR, UserRole.STAFF, UserRole.MENTOR]

        participant_roles = _entrepreneur_specific_alumni_filter(
            participant_roles, request)

        participant_roles = _entrepreneur_specific_finalist_filter(
            participant_roles, request)

        user_program_roles_as_participant = ProgramRole.objects.filter(
            programrolegrant__person=request.user,
            user_role__name__in=participant_roles
        )

        program_groups = Program.objects.filter(
            programrole__in=user_program_roles_as_participant
        ).values_list(
            'mentor_program_group', flat=True).distinct()
        program_families = ProgramFamily.objects.filter(
            programs__mentor_program_group__in=program_groups
        ).prefetch_related('programs').distinct()
        facet_filters = _facet_filters(program_families)
        if len(facet_filters) > 0:
            return " OR ".join(facet_filters)
        else:
            return IS_CONFIRMED_MENTOR_FILTER


def _entrepreneur_specific_finalist_filter(roles, request):
    if is_entrepreneur(request.user):
        has_current_finalist_roles = ProgramRoleGrant.objects.filter(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS,
            program_role__user_role__name=UserRole.FINALIST,
            person=request.user
        ).exists()

        if has_current_finalist_roles:
            roles.append(UserRole.FINALIST)

    return roles


def _entrepreneur_specific_alumni_filter(roles, request):
    if is_entrepreneur(request.user):
        has_current_alum_roles = ProgramRoleGrant.objects.filter(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS,
            program_role__user_role__name=UserRole.ALUM,
            person=request.user
        ).exists()

        if has_current_alum_roles:
            roles.append(UserRole.ALUM)

    return roles


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


def _build_filter(*args):
    return " AND ".join(args)
