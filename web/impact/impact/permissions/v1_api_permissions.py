from rest_framework.permissions import IsAuthenticated

from accelerator_abstract.models.base_program import ACTIVE_PROGRAM_STATUS
from accelerator.models.user_role import UserRole

from accelerator_abstract.models.base_user_utils import (
    is_employee,
    is_expert,
)
from impact.permissions import (
    settings,
    BasePermission,
)


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DEFAULT_PERMISSION_DENIED_DETAIL = ("You do not have permission to perform "
                                    "this action.")


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


class OfficeHourMentorPermission(BasePermission):
    # User has permission to act as mentor on this office hour

    def has_object_permission(self, request, view, office_hour):
        return (is_employee(request.user) or
                office_hour.mentor == request.user)


class OfficeHourFinalistPermission(BasePermission):
    # User has permission to act as finalist on this office hour

    def has_object_permission(self, request, view, office_hour):
        return (is_employee(request.user) or
                office_hour.finalist == request.user)


class IsExpertUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                is_expert(request.user))

class ReserveOfficeHourPermission(V1APIPermissions):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) or
                can_reserve_office_hour(request.user))

def can_reserve_office_hour(user):
    return user.programrolegrant_set.filter(
        program_role__user_role__name__in=[UserRole.FINALIST, UserRole.AIR, UserRole.ALUM],
        program_role__program__program_status=ACTIVE_PROGRAM_STATUS).exists()

