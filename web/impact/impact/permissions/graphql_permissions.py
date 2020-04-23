from accelerator.models import (
    EntrepreneurProfile,
    ExpertProfile,
    UserRole,
)
from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import ACTIVE_PROGRAM_STATUS


def visible_roles(current_user):
    basic_user_roles = [
        UserRole.FINALIST,
        UserRole.AIR,
        UserRole.MENTOR,
        UserRole.PARTNER,
        UserRole.ALUM
    ]
    basic_visible_roles = [UserRole.FINALIST, UserRole.STAFF, UserRole.ALUM]

    current_logged_in_user_roles = list(
        current_user.programrolegrant_set.filter(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS
        ).values_list(
            'program_role__user_role__name', flat=True).distinct()
    )
    if not current_logged_in_user_roles:
        return [UserRole.STAFF]
    if set(basic_user_roles).intersection(current_logged_in_user_roles):
        return basic_visible_roles + [UserRole.MENTOR]
    if UserRole.JUDGE in current_logged_in_user_roles:
        return basic_visible_roles


def can_view_profile(profile_user, roles):
    return profile_user.programrolegrant_set.filter(
        program_role__user_role__name__in=roles,
        program_role__program__program_status=ACTIVE_PROGRAM_STATUS
    ).exists()


def can_view_entrepreneur_profile(current_user, profile_user):
    if not is_employee(current_user):
        roles = visible_roles(current_user)
        return can_view_profile(profile_user, roles)
    return True
