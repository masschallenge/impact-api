import graphene
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

from impact.utils import compose_filter


class ExpertProfileType(DjangoObjectType):
    current_mentees = graphene.List(StartupMentorRelationshipType)
    previous_mentees = graphene.List(StartupMentorRelationshipType)
    image_url = graphene.String()
    office_hours_url = graphene.String()
    program_interests = graphene.List(graphene.String)
    available_office_hours = graphene.Boolean()

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
            slugs = _get_slugs(self, info)
            return "/officehours/list/{family_slug}/{program_slug}/".format(
                family_slug=slugs[0],
                program_slug=slugs[1]) + (
                '?mentor_id={mentor_id}'.format(
                    mentor_id=self.user.id))

    def resolve_current_mentees(self, info, **kwargs):
        return _get_mentees(self.user, ACTIVE_PROGRAM_STATUS)

    def resolve_previous_mentees(self, info, **kwargs):
        return _get_mentees(self.user, ENDED_PROGRAM_STATUS)


def _get_slugs(self, info, **kwargs):
    role_grant = self.user.programrolegrant_set.filter(
            program_role__user_role__name=UserRole.MENTOR,
            program_role__program__end_date__gte=datetime.now()
            ).distinct()
    user = info.context.user
    for mentor_program in role_grant:
        mentor_program_view = mentor_program.program_role.program
        if(mentor_program_view in _get_user_programs(user)):
            return (
                mentor_program_view.program_family.url_slug,
                mentor_program_view.url_slug
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
