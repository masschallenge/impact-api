from accelerator_abstract.models.base_user_utils import (
    is_employee,
    is_expert,
)
from impact.permissions import (
    settings,
    BasePermission,
)
from rest_framework.permissions import IsAuthenticated

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


def can_view_user_details_page(request):
    user_id = request.parser_context['kwargs'].get('pk', '')
    if user_id and request.method in SAFE_METHODS:
        return str(user_id) == str(request.user.id)


class V1APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return (is_employee(request.user) or
                request.user.groups.filter(
                    name=settings.V1_API_GROUP).exists())


class UserDetailViewPermission(V1APIPermissions):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) or
                can_view_user_details_page(request))


class IsExpertUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                is_expert(request.user))
