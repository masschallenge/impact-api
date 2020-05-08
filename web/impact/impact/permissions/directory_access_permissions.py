from . import BasePermission
from accelerator_abstract.models import ACTIVE_PROGRAM_STATUS
from accelerator.models import UserRole
from accelerator_abstract.models.base_user_utils import is_employee
from accelerator_abstract.models.base_permission_checks import (
    base_accelerator_check
)


class DirectoryAccessPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        allowed_roles = UserRole.FINALIST_USER_ROLES + [
            UserRole.MENTOR, UserRole.ALUM
        ]
        return (
            request.user.programrolegrant_set.filter(
                program_role__program__program_status=ACTIVE_PROGRAM_STATUS,
                program_role__user_role__name__in=allowed_roles,
            ).exists() or
            is_employee(request.user) or
            base_accelerator_check(request.user)
        )
