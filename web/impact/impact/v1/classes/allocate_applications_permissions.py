from rest_framework.permissions import BasePermission

class AllocateApplicationsPermissions(BasePermission):
    authenticated_users_only = True
    
    def has_permission(self, request, view):
        request_judge_id = int(request.parser_context['kwargs']['judge_id'])
        if request.user.id == request_judge_id:
            return True
        return super().has_permission(request, view)
