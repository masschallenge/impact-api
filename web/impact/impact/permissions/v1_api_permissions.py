
from rest_framework.permissions import IsAuthenticated


from accelerator_abstract.models.base_user_utils import (
    is_employee,
    is_expert,
)
from accelerator.models import UserRole
from impact.permissions import (
    settings,
    BasePermission,
)

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DEFAULT_PERMISSION_DENIED_DETAIL = ("You do not have permission to perform "
                                    "this action.")
CREATE_PERMISSION_DENIED_DETAIL = ("You do not have permission to create "
                                   "this office hour")
EDIT_PERMISSION_DENIED_DETAIL = ("You do not have permission to edit this "
                                 "office hour")
RESERVE_PERMISSION_DENIED_DETAIL = ("You do not have permission to reserve "
                                    "this office hour")
CANCEL_SESSION_PERMISSION_DENIED_DETAIL = ("You do not have permission to "
                                           "cancel this office hour")
CANCEL_RESERVATION_PERMISSION_DENIED_DETAIL = ("You do not have permission "
                                               "to cancel this session")
OFFICE_HOUR_RESERVERS = [UserRole.FINALIST, UserRole.AIR, UserRole.ALUM]


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
    message = CANCEL_SESSION_PERMISSION_DENIED_DETAIL

    def has_object_permission(self, request, view, office_hour):
        return (is_employee(request.user) or
                office_hour.mentor == request.user)


class OfficeHourFinalistPermission(BasePermission):
    # User has permission to act as finalist on this office hour
    message = CANCEL_RESERVATION_PERMISSION_DENIED_DETAIL

    def has_object_permission(self, request, view, office_hour):
        return (is_employee(request.user) or
                office_hour.finalist == request.user)


class IsExpertUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and
                is_expert(request.user))


class OfficeHourPermission(IsAuthenticated):
    def has_permission(self, request, view):
        self.get_message(request)
        roles = [UserRole.MENTOR, UserRole.AIR]
        return super().has_permission(request, view) and (
            is_employee(request.user) or
            request.user.programrolegrant_set.filter(
                program_role__user_role__name__in=roles,
                program_role__program__program_status='active',
            ).exists())

    def has_object_permission(self, request, view, office_hour):
        is_reserved = office_hour.finalist
        return (is_employee(request.user) or
                office_hour.mentor == request.user and not is_reserved)

    def get_message(self, request):
        dict = {'POST': CREATE_PERMISSION_DENIED_DETAIL,
                'PATCH': EDIT_PERMISSION_DENIED_DETAIL}
        self.message = dict.get(request.method,
                                DEFAULT_PERMISSION_DENIED_DETAIL)
