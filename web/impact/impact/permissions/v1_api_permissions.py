from accelerator_abstract.models.base_user_utils import is_employee
from accelerator_abstract.models.base_user_role import is_finalist_user
from impact.permissions import (
    settings,
    BasePermission)


class V1APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V1_API_GROUP).exists() or is_employee(
                request.user) or is_finalist_user(request.user)
