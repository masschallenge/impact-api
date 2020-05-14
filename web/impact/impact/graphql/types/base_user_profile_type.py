from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar

from accelerator.models import (
    BaseProfile,
    StartupRole,
    UserRole
)
from accelerator_abstract.models.base_user_utils import is_employee
from impact.utils import (
    get_user_program_and_startup_roles,
)


class BaseUserProfileType(DjangoObjectType):
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
