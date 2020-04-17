import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar

from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from accelerator.models import (
    CONFIRMED_RELATIONSHIP,
    ExpertProfile,
    Program,
    ProgramRole,
    StartupRole,
    UserRole
)
from accelerator_abstract.models import (
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS,
    HIDDEN_PROGRAM_STATUS,
    UPCOMING_PROGRAM_STATUS
)
from accelerator_abstract.models.base_user_utils import is_employee
from impact.graphql.types import StartupMentorRelationshipType

from impact.utils import (
    compose_filter,
    get_user_program_and_startup_roles,
)
from impact.v1.helpers.profile_helper import (
    latest_program_id_for_each_program_family,
)


class ExpertProfileType(DjangoObjectType):
    current_mentees = graphene.List(StartupMentorRelationshipType)
    previous_mentees = graphene.List(StartupMentorRelationshipType)
    image_url = graphene.String()
    office_hours_url = graphene.String()
    program_interests = graphene.List(graphene.String)
    available_office_hours = graphene.Boolean()
    program_roles = GenericScalar()
    confirmed_mentor_program_families = graphene.List(graphene.String)

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

    def resolve_image_url(obj, info, **kwargs):
        return obj.image and obj.image.url

    def resolve_program_interests(obj, info, **kwargs):
        return obj.interest_categories.all().values_list(
            'program__program_family__name', flat=True).distinct()

    def resolve_available_office_hours(obj, info, **kwargs):
        user = info.context.user
        filter_kwargs = {
            'finalist__isnull': True,
        }
        now = timezone.now()
        if not user.is_staff and user != obj.user and not user.is_superuser:
            filter_kwargs['program__in'] = _get_user_programs(user)
        future_datetime_filter = Q(start_date_time__gte=now)
        return obj.user.mentor_officehours.filter(**filter_kwargs).filter(
            future_datetime_filter).exists()

    def resolve_office_hours_url(obj, info, **kwargs):
        if obj.user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR
        ).exists():
            role_grants = obj.user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR,
                program_role__program__end_date__gte=datetime.now()
            ).distinct()

            latest_grant = obj.user.programrolegrant_set.filter(
                program_role__user_role__name=UserRole.MENTOR
            ).latest('created_at')
            latest_mentor_program = latest_grant.program_role.program
            user = info.context.user
            mentor_program = [
                role_grant.program_role.program for role_grant in role_grants
                if role_grant.program_role.program in _get_user_programs(user)
            ]
            if mentor_program or latest_mentor_program:
                slugs = _get_slugs(obj, mentor_program, latest_mentor_program)
                urlpath = "/officehours/list/{family_slug}/{program_slug}/"
                return urlpath.format(
                    family_slug=slugs[0],
                    program_slug=slugs[1]) + (
                    '?mentor_id={mentor_id}'.format(
                        mentor_id=obj.user.id))

    def resolve_current_mentees(obj, info, **kwargs):
        return _get_mentees(obj.user, ACTIVE_PROGRAM_STATUS)

    def resolve_previous_mentees(obj, info, **kwargs):
        return _get_mentees(obj.user, ENDED_PROGRAM_STATUS)

    def resolve_confirmed_mentor_program_families(obj, info, **kwargs):
        program_families = _visible_confirmed_mentor_role_grants(obj)
        program_ids = latest_program_id_for_each_program_family()
        return program_families.filter(
            program_role__program__pk__in=program_ids
        ).exclude(
            program_role__program__program_family__name=obj.home_program_family
        ).values_list(
            'program_role__program__program_family__name',
            flat=True).distinct()

    def resolve_program_roles(self, info, **kwargs):
        """
        Returns the program roles and startup roles for this user
        Note that name is deceptive, since startup roles are included in the
        return but not mentioned in the name. This cannot be fixed here
        without changing GraphQL queries on the front end.
        """
        user_roles_of_interest = [UserRole.FINALIST, UserRole.ALUM]
        startup_roles_of_interest = StartupRole.WINNER_STARTUP_ROLES
        if is_employee(info.context.user):
            startup_roles_of_interest += [StartupRole.ENTRANT]
        return get_user_program_and_startup_roles(
            self.user, user_roles_of_interest, startup_roles_of_interest)


def _get_slugs(obj, mentor_program, latest_mentor_program, **kwargs):
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


def _visible_confirmed_mentor_role_grants(expert_profile):
    return expert_profile.user.programrolegrant_set.filter(
        program_role__user_role__name=UserRole.MENTOR).exclude(
        program_role__program__program_status__in=[
            HIDDEN_PROGRAM_STATUS,
            UPCOMING_PROGRAM_STATUS]
    ).prefetch_related(
        'program_role__program',
        'program_role__program__program_family'
    )
