# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ast import literal_eval
import logging

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission

from accelerator.apps import AcceleratorConfig
from accelerator.models import Clearance
from accelerator_abstract.models.base_clearance import (
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LOGGER_FAILED_INSUFFICIENT_CLEARANCE_MSG,
    CLEARANCE_LOGGER_SUCCESS_MSG,
)
from impact.utils import model_name_case

from accelerator_abstract.models.base_user_utils import is_entrepreneur
from accelerator_abstract.models import ACTIVE_PROGRAM_STATUS
from accelerator.models import UserRole
from accelerator_abstract.models.base_user_utils import is_employee

logger = logging.getLogger(__file__)
User = get_user_model()

METHOD_TO_ACTION = {
    "POST": "add",
    "GET": "view",
    "HEAD": "view",
    "OPTIONS": "view",
    "PUT": "change",
    "PATCH": "change",
    "DELETE": "delete",
}


# FIXME: function definitions duplicated from mc.permission_checks

def _log_access_attempt(cleared, user, level, program_family):
    if cleared:
        _log_sufficient_clearance(level, program_family, user)
    else:
        _log_insufficient_clearance(level, program_family, user)


def _log_sufficient_clearance(level, program_family, user):
    logger.info(CLEARANCE_LOGGER_SUCCESS_MSG.format(
        user=user, program_family=program_family, level=level))


def _log_insufficient_clearance(level, program_family, user):
    logger.info(CLEARANCE_LOGGER_FAILED_INSUFFICIENT_CLEARANCE_MSG.format(
        user=user, program_family=program_family, level=level))

# end duplicated definitions


def global_operations_manager_check(user, program_family=None):
    cleared = Clearance.objects.check_clearance(
        user, CLEARANCE_LEVEL_GLOBAL_MANAGER, program_family)
    _log_access_attempt(cleared, user,
                        CLEARANCE_LEVEL_GLOBAL_MANAGER, program_family)
    return cleared


class V0APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V0_API_GROUP).exists()


class DirectoryAccessPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        allowed_roles = UserRole.FINALIST_USER_ROLES + [
            UserRole.MENTOR, UserRole.ALUM
        ]
        return request.user.programrolegrant_set.filter(
            program_role__program__program_status=ACTIVE_PROGRAM_STATUS,
            program_role__user_role__name__in=allowed_roles,
        ).exists() or is_employee(request.user)


class V1APIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V1_API_GROUP).exists()


class V1ConfidentialAPIPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V1_CONFIDENTIAL_API_GROUP).exists()


def method_to_perm(method):
    return "%(app)s.{}_%(model_name)s".format(METHOD_TO_ACTION[method])


class DynamicModelPermissions(BasePermission):
    authenticated_users_only = True

    def has_permission(self, request, view):
        model = view.kwargs.get('model', '').lower()
        related_model = view.kwargs.get('related_model', '').lower()
        model_name = model_name_case(model, related_model)
        kwargs = {'app': AcceleratorConfig.name, 'model_name': model_name}
        perm = method_to_perm(request.method) % kwargs
        return (
            request.user and (
                request.user.is_authenticated or (
                    not self.authenticated_users_only)) and (
                request.user.has_perms([perm]))
        )

    def get_field_level_perms(self, app_label, model_name):
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
        return (
            Permission
            .objects
            .filter(content_type=ct)
            .exclude(codename='view_{}'.format(model_name))
            .exclude(codename='add_{}'.format(model_name))
            .exclude(codename='change_{}'.format(model_name))
            .exclude(codename='delete_{}'.format(model_name))
        )

    def decompose_perm(self, perm_codename):
        # permissions come in the structure:
        # app_label.action_modelName_fieldName_boolean
        # fieldName *may* have underscores in it!
        perm_struct, boolean_str = perm_codename.rsplit('_', 1)
        action, perm_model, field = perm_struct.split('_', 2)
        return action, perm_model, field, boolean_str

    def action_matches(self, action, request):
        if action == METHOD_TO_ACTION.get(request.method):
            return True
        return False

    def convert_string_to_bool(self, text_value):
        try:
            boolean_value = literal_eval(text_value.title())
        except:  # noqa: E722 # pragma: no cover
            # Regarding coverage, see AC-4573
            raise PermissionDenied  # pragma: no cover
        return boolean_value

    def has_object_permission(self, request, view, obj):
        model = view.kwargs.get('model', '').lower()
        related_model = view.kwargs.get('related_model', '').lower()
        model_name = model_name_case(model, related_model)
        app_label = obj._meta.app_label
        # This needs to be revised.  See AC-4573
        for permission in self.get_field_level_perms(app_label, model_name):
            action, perm_model, field, boolean_str = (
                self.decompose_perm(permission.codename))
            if hasattr(obj, field):
                if self.action_matches(action, request):
                    boolean_value = self.convert_string_to_bool(boolean_str)
                    permission_code = (
                        '{}.{}'.format(app_label, permission.codename))
                    if getattr(obj, field, None) is boolean_value:
                        if not get_user(request).has_perm(permission_code):
                            return False  # pragma: no cover
                    # some other value is in place,
                    # so we don't require permissions
        return True
