import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from django.utils import timezone
from datetime import datetime
from accelerator.models import (
    ExpertProfile,
    UserRole,
    ProgramRole,
    Program,
    CONFIRMED_RELATIONSHIP,
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS,
)
from impact.graphql.types import StartupMentorRelationshipType
from django.db.models import Q

from impact.utils import (
    get_user_startup_prg_role_by_program_family, combine_prg_roles,
    compose_filter, get_user_prg_role_by_program_family,
)

class ExpertProfileType(DjangoObjectType):
    current_mentees = graphene.List(StartupMentorRelationshipType)
    previous_mentees = graphene.List(StartupMentorRelationshipType)
    image_url = graphene.String()
    office_hours_url = graphene.String()
    program_interests = graphene.List(graphene.String)
    available_office_hours = graphene.Boolean()
    program_roles = GenericScalar()

    class Meta:
        model = ExpertProfile
        only_fields = (
            'title',
            'company',
            'phone',
            'twitter_handle',
            'linked_in_url',
            'personal_website_url',
            'bio',
            'expert_category',
            'primary_industry',
            'additional_industries',
            'home_program_family',
            'user',
            'functional_expertise',
            'interest_categories',
            'judge_type',
            'mentor_type',
        )

    def resolve_image_url(self, info, **kwargs):
        return self.image and self.image.url

    def resolve_program_interests(self, info, **kwargs):
        return self.interest_categories.all().values_list(
            'program__program_family__name', flat=True).distinct()

    def resolve_available_office_hours(self, info, **kwargs):
        user = info.context.user
        filter_kwargs = {
            'finalist__isnull': True,
        }
        now = timezone.now()
        if not user.is_staff and user != self.user and not user.is_superuser:
            filter_kwargs['program__in'] = _get_user_programs(user)
        future_datetime_filter = Q(start_date_time__gte=now)
        return self.user.mentor_officehours.filter(**filter_kwargs).filter(
            future_datetime_filter).exists()

    def resolve_office_hours_url(self, info, **kwargs):
        if self.user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR
        ).exists():
            role_grants = self.user.programrolegrant_set.filter(
            program_role__user_role__name=UserRole.MENTOR,
            program_role__program__end_date__gte=datetime.now()
            ).distinct()

            latest_grant = self.user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR
            ).latest('created_at')
            latest_mentor_program = latest_grant.program_role.program
            user = info.context.user
            mentor_program = [role_grant.program_role.program for role_grant in role_grants
                              if role_grant.program_role.program in _get_user_programs(user)]
            if mentor_program or latest_mentor_program:
                slugs = _get_slugs(self, mentor_program, latest_mentor_program)
                return "/officehours/list/{family_slug}/{program_slug}/".format(
                    family_slug=slugs[0],
                    program_slug=slugs[1]) + (
                    '?mentor_id={mentor_id}'.format(
                        mentor_id=self.user.id))

    def resolve_current_mentees(self, info, **kwargs):
        return _get_mentees(self.user, ACTIVE_PROGRAM_STATUS)

    def resolve_previous_mentees(self, info, **kwargs):
        return _get_mentees(self.user, ENDED_PROGRAM_STATUS)

    """
    fetch a program role assigned to an user and those assigned to the startups
    the user belong to

    Time, Space, Query Complexity
    Query: amount to the query complexity of the two helper function that
    access the DB (see functions for query comp analysis for each)

    Time/Space amount to time and space complexity of the three helper functions
    (see functions for time/space comp analysis for each)
    """
    def resolve_program_roles(self, info, **kwargs):
        roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        user_prg_roles = get_user_prg_role_by_program_family(
            self.user, roles_of_interest)
        startup_prg_roles = get_user_startup_prg_role_by_program_family(
           self.user
        )
        return combine_prg_roles(
            user_prg_roles=user_prg_roles, startup_prg_roles=startup_prg_roles
        )


def _get_slugs(self, mentor_program, latest_mentor_program, **kwargs):
    if mentor_program:
        return (
            mentor_program[0].program_family.url_slug,
            mentor_program[0].url_slug,
        )
    return (
            latest_mentor_program.program_family.url_slug,
            latest_mentor_program.url_slug,
        )

def _get_user_programs(user):
    # todo: refactor this and move it to a sensible place
    # todo: test this
    participant_roles = UserRole.FINALIST_USER_ROLES
    user_program_roles_as_participant = ProgramRole.objects.filter(
        programrolegrant__person=user,
        user_role__name__in=participant_roles
    )
    return Program.objects.filter(
        programrole__in=user_program_roles_as_participant).distinct()


def _get_mentees(user, program_status):
    mentee_filter = compose_filter([
        'startup_mentor_tracking',
        'program',
        'program_status'
    ], program_status)
    return user.startupmentorrelationship_set.filter(
        status=CONFIRMED_RELATIONSHIP,
        **mentee_filter
    ).order_by('-startup_mentor_tracking__program__start_date')

