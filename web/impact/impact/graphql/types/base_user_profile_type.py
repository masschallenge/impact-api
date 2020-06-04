from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from itertools import chain
import graphene

from accelerator.models import (
    BaseProfile,
    StartupRole,
    Clearance,
    UserRole,
    Location
)

from impact.graphql.types import LocationType
from accelerator_abstract.models.base_user_utils import is_employee
from ...utils import get_user_program_and_startup_roles


class BaseUserProfileType(DjangoObjectType):
    office_hour_locations = graphene.List(LocationType)
    program_roles = GenericScalar()

    class Meta:
        model = BaseProfile

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

    def resolve_office_hour_locations(self, info, **kwargs):
        family_ids = Clearance.objects.clearances_for_user(
            self.user
        ).values_list("program_family", flat=True)
        desired_user_roles = [
            UserRole.MENTOR, UserRole.FINALIST, UserRole.AIR]
        program_family_ids = self.user.programrolegrant_set.filter(
            program_role__program__program_status="active",
            program_role__user_role__name__in=desired_user_roles
            ).values_list(
                "program_role__program__program_family", flat=True
                ).distinct()
        ids = list(set(chain(family_ids, program_family_ids)))
        remote = Location.objects.filter(name='Remote').first()
        result = Location.objects.filter(
            programfamilylocation__program_family_id__in=ids,).exclude(
                name='Remote'
            ).distinct()
        locations = list(result)
        locations.append(remote)

        return locations
