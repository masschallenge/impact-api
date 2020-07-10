from django.conf import settings
from rest_framework.permissions import BasePermission


class V0APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V0_API_GROUP).exists()
