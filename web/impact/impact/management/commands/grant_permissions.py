# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


# -*- coding: utf-8 -*-

"""Add permissions for proxy model.

This is needed because of the bug https://code.djangoproject.com/ticket/11154
in Django (as of 1.6, it's not fixed).

When a permission is created for a proxy model, it actually creates if for it's
base model app_label (eg: for "article" instead of "about", for the About proxy
model).

What we need, however, is that the permission be created for the proxy model
itself, in order to have the proper entries displayed in the admin.

"""

from __future__ import unicode_literals, absolute_import, division
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "Grant permissions for api objects."

    def add_arguments(self, parser):
        parser.add_argument('user_email', nargs='?', type=str)
        parser.add_argument('permission_names', nargs='?', type=str)

    def handle(self, *args, **options):
        permission_names = options.get('permission_names', "").split(',')
        user_email = options.get('user_email')
        User = get_user_model()
        user = User.objects.get(email=user_email)
        for permission_name in permission_names:
            if permission_name == "v0_api":
                self.grant_v0_perms(user)
            else:
                perm, model = permission_name.split('_')
                content_type = ContentType.objects.get(model=model)
                permission, _ = Permission.objects.get_or_create(
                    codename=permission_name,
                    content_type=content_type)
                user.user_permissions.add(permission)
                print(
                    "granting permission %s to %s" % (
                        permission_name, user.email))
        user.save()

    def grant_v0_perms(self, user):
        group, created = Group.objects.get_or_create(
            name=settings.V0_API_GROUP)
        user.groups.add(group)
        print(
            "granting permission to the v0 api to %s" % user.email)
