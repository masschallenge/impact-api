from accelerator_abstract.models.base_user_utils import is_employee
from impact.permissions import (
    settings,
    BasePermission,
)

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


def can_view_user_details_page(request):
    # importing here to avoid circular import
    from impact.v1.views.user_detail_view import UserDetailView  # noqa: E402
    if request.resolver_match.url_name == UserDetailView.view_name:
        user_id = request.parser_context['kwargs'].get('pk', '')
        if user_id and request.method in SAFE_METHODS:
            return str(user_id) == str(request.user.id)


class V1APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return (is_employee(request.user) or
                can_view_user_details_page(request) or
                request.user.groups.filter(name=settings.V1_API_GROUP).exists())
