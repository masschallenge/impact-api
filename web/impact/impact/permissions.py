# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ast import literal_eval

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission

User = get_user_model()


class V0APIPermissions(BasePermission):

    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V0_API_GROUP).exists()


class V1APIPermissions(BasePermission):

    authenticated_users_only = True

    def has_permission(self, request, view):
        return request.user.groups.filter(
            name=settings.V1_API_GROUP).exists()


class DynamicModelPermissions(BasePermission):
    perms_map = {
        'GET': ['%(app)s.view_%(model_name)s'],
        'OPTIONS': ['%(app)s.view_%(model_name)s'],
        'HEAD': ['%(app)s.view_%(model_name)s'],
        'POST': ['%(app)s.add_%(model_name)s'],
        'PUT': ['%(app)s.change_%(model_name)s'],
        'PATCH': ['%(app)s.change_%(model_name)s'],
        'DELETE': ['%(app)s.delete_%(model_name)s'],
    }

    authenticated_users_only = True

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        model_name = view.kwargs.get('model', "").lower()
        app_label = 'mc'
        kwargs = {'app': app_label, 'model_name': model_name}
        perms = [perm % kwargs for perm in self.perms_map[request.method]]
        return (
            request.user and (
                is_authenticated(request.user) or (
                    not self.authenticated_users_only)) and (
                request.user.has_perms(perms))
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
        if ((request.method in ('POST') and action == 'add') or (
            request.method in ('GET', 'HEAD', 'OPTIONS') and (
                action == 'view')) or (
            request.method in (
                'PUT', 'PATCH') and (
                action == 'change')) or (
                request.method in ('DELETE') and (action == 'delete'))):
            # the permission applies to our case
            return True
        return False

    def convert_string_to_bool(self, text_value):
        try:
            boolean_value = literal_eval(text_value.title())
        except:
            # not a bool? unequivocably reject permission
            raise PermissionDenied
        return boolean_value

    def has_object_permission(self, request, view, obj):
        model_name = view.kwargs.get('model', "").lower()
        app_label = 'mc'
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
                            return False
                    # some other value is in place,
                    # so we don't require permissions
        return True
