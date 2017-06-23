# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from __future__ import unicode_literals, absolute_import, division
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "Grant permissions for api objects."

    def add_arguments(self, parser):
        parser.add_argument("user_email", nargs="?", type=str)
        parser.add_argument("permission_names", nargs="?", type=str)

    def handle(self, *args, **options):
        permission_names = options.get("permission_names", "").split(",")
        user_email = options.get("user_email")
        User = get_user_model()
        user = User.objects.get(email=user_email)
        for permission_name in permission_names:
            perm, model = permission_name.split("_")
            content_type = ContentType.objects.filter(model=model).first()
            if content_type:
                grant_model_permission(permission_name, content_type, user)
            else:
                grant_group_permission(permission_name, user)
        user.save()


def grant_model_permission(permission_name, content_type, user):
    permission, _ = Permission.objects.get_or_create(
        codename=permission_name,
        content_type=content_type)
    user.user_permissions.add(permission)
    print("granting model permission {name} to {email}".format(
            name=permission_name,
            email=user.email))


def grant_group_permission(group_name, user):
    group = Group.objects.filter(name=group_name).first()
    if not group:
        response = input("Create group name {}? ".format(group_name))
        if response.lower() not in ["y", "yes"]:
            print("Ignoring requested permissions: {}".format(group_name))
            return
        group = Group.objects.create(name=group_name)
    user.groups.add(group)
    print("granting {email} add to group {group}".format(email=user.email,
                                                         group=group_name))
