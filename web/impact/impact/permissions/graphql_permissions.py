from mc.models import UserRole
from accelerator.models import ACTIVE_PROGRAM_STATUS
from accelerator_abstract.models.base_user_utils import is_employee


BASIC_ALLOWED_USER_ROLES = [
    UserRole.FINALIST,
    UserRole.AIR,
    UserRole.MENTOR,
    UserRole.PARTNER,
    UserRole.ALUM
]

BASIC_VISIBLE_USER_ROLES = [UserRole.FINALIST, UserRole.STAFF, UserRole.ALUM]


def check_for_no_user_role(logged_in_user_roles):
    count = len(logged_in_user_roles) == 1
    return not logged_in_user_roles or count and not logged_in_user_roles[0]


def check_for_basic_user_roles(logged_in_user_roles):
    return any(
        [role in BASIC_ALLOWED_USER_ROLES for role in logged_in_user_roles]
    )


def visible_roles(current_user):
    current_logged_in_user_roles = list(
        current_user.programrolegrant_set.filter(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS
        ).values_list('program_role__user_role__name', flat=True).distinct())
    if check_for_no_user_role(current_logged_in_user_roles):
        return [UserRole.STAFF]
    if check_for_basic_user_roles(current_logged_in_user_roles):
        return BASIC_VISIBLE_USER_ROLES + [UserRole.MENTOR]
    if UserRole.JUDGE in current_logged_in_user_roles:
        return BASIC_VISIBLE_USER_ROLES


def can_view_profile(profile_user, roles):
    return profile_user.programrolegrant_set.filter(
        program_role__user_role__name__in=roles
    ).exists()


def can_view_entrepreneur_profile(current_user, profile_user):
    if not is_employee(current_user):
        roles = visible_roles(current_user)
        return can_view_profile(profile_user, roles)
    return True
