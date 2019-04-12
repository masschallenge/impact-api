# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from rest_framework.authtoken.models import Token


logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("creating new token for user %s" % instance.email)
        Token.objects.create(user=instance)
