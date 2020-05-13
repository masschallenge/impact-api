from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar

from django.db.models import Q
from accelerator_abstract.models.base_user_utils import is_employee
from accelerator_abstract.models.base_user_role import (
    is_finalist_user,
    is_mentor,
)
from accelerator.models import (
    BaseProfile,
    StartupRole,
    UserRole,
    ProgramRoleGrant
)
from accelerator_abstract.models.base_user_utils import is_employee
from impact.utils import (
    get_user_program_and_startup_roles,
)
from impact.v1.views.utils import (
    map_data,
)


class BaseUserProfileType(DjangoObjectType):
    program_roles = GenericScalar()
    program_role_grants = GenericScalar()

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

    def resolve_program_role_grants(self, info, **kwargs):
        """
        Returns the program grants for this user
        """
        results = map_data(
            ProgramRoleGrant,
            Q(person_id=self.user.pk,
              program_role__program__program_status__in=['active', 'upcoming']),
            'id',
            [
                'id',
                'program_role__program__name',
                'program_role__program__start_date',
                'program_role__program__end_date',
                'program_role__user_role__name',
                'program_role__program__program_overview_link',
            ],
            [
                'id',
                'program_name',
                'program_start_date',
                'program_end_date',
                'user_role_name',
                'program_overview_link',
            ]
        )

        for data in results:
            data['program_start_date'] = data['program_start_date'].isoformat()
            data['program_end_date'] = data['program_end_date'].isoformat()

        return {"results": results, "is_mentor": is_mentor(self.user),
                "is_finalist": is_finalist_user(self.user),
                "is_employee": is_employee(self.user)}
