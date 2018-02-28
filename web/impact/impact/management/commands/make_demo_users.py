# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


def create_users_and_stealth_view_perm():
    # Create the Permission object
    stealth_view_perm, _ = Permission.objects.get_or_create(
        content_type=ContentType.objects.get(
            app_label='accelerator', model="startup"),
        codename="view_startup_stealth_mode_true",
        name="Can view Startups in Stealth Mode"
    )
    startup_view_perm, _ = Permission.objects.get_or_create(
        content_type=ContentType.objects.get(
            app_label='accelerator', model="startup"),
        codename="view_startup"
    )

    # Create the two users (they may already exist; check first)
    User = get_user_model()
    m_email = "marketing-site@example.com"
    s_email = "salesforce@example.com"
    try:
        marketing_user = User.objects.get(email=m_email)
    except User.DoesNotExist:
        marketing_user = User.objects.create_user(m_email, "x")
    try:
        salesforce_user = User.objects.get(email=s_email)
    except User.DoesNotExist:
        salesforce_user = User.objects.create_user(s_email, "x")

    # Give them the relevant permissions
    marketing_user.user_permissions.add(startup_view_perm.pk)
    salesforce_user.user_permissions.add(startup_view_perm.pk)
    salesforce_user.user_permissions.add(stealth_view_perm.pk)
    return (marketing_user, salesforce_user)


class Command(BaseCommand):
    help = "Create Marketing-site and Salesforce users for demo"

    def handle(self, *args, **options):
        print(create_users_and_stealth_view_perm())
