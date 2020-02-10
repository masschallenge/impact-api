from accelerator_abstract.models.base_user_utils import is_employee
from impact.permissions import (
    settings,
    BasePermission,
)

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


def is_object_owner(request, user_id):
    if user_id and request.method in SAFE_METHODS:
        return str(user_id) == str(request.user.id)


class V1APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        user_id = request.parser_context['kwargs'].get('pk', '')

        return request.user.groups.filter(
            name=settings.V1_API_GROUP
        ).exists() or is_employee(request.user) or is_object_owner(request, user_id)
