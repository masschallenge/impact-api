from impact.permissions import (
    settings,
    BasePermission)


class V1ConfidentialAPIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V1_CONFIDENTIAL_API_GROUP).exists()
