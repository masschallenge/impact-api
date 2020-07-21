from django.conf import settings
from accelerator.models import UserRole
from accelerator_abstract.models.base_user_utils import is_employee

PUBLIC = 'public'
STAFF = 'staff'
FINALISTS_AND_STAFF = 'finalists and staff'


def get_jwt_cookie(request):
    cookie_name = settings.JWT_AUTH.get('JWT_AUTH_COOKIE')
    if cookie_name:
        return request.COOKIES.get(cookie_name)
    return None


def get_user_privacy_type(user):
    if is_employee(user):
        return STAFF
    if user.programrolegrant_set.filter(
            program_role__user_role__name=UserRole.FINALIST
    ).exists():
        return FINALISTS_AND_STAFF
    return PUBLIC


def can_view_private_data(user, type_requirement):
    user_privacy_type = get_user_privacy_type(user)
    if user_privacy_type == STAFF:
        return True
    if type_requirement == PUBLIC:
        return True
    return type_requirement == user_privacy_type
