# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    Organization,
    Partner,
    Startup,
)
from impact.v1.metadata import ImpactMetadata

INVALID_KEYS_ERROR = ("Received invalid key(s): {invalid_keys}. "
                      "Valid keys are: {valid_keys}.")
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DAWN_OF_TIME = "2010-01-01T00:00:00Z"

class OrganizationHistoryView(APIView):
    model = Organization
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        result = {
            "history": [self._created_event()]
        }
        return Response(result)

    def _created_event(self):
        earliest, latest = self._created_datetime()
        return {
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": "created",
            "description": ""
            }

    def _created_datetime(self):
        startup = self.instance.startup_set.first()
        if startup:
            return _created_datetimes(startup, Startup)
        partner = self.instance.partner_set.first()
        if partner:
            return _created_datetimes(partner, Partner)
        return _created_datetimes(self.instance, Organization)


def _created_datetimes(instance, klass):
    if instance.created_at is not None:
        return (instance.created_at, instance.created_at)
    if hasattr(instance, "created_datetime"):
        if instance.created_datetime is not None:
            return (instance.created_datetime,
                    instance.created_datetime)
        return (_previous_created_datetime(instance, klass),
                _next_created_datetime(instance, klass))
    next_instance = klass.objects.filter(id__gt=instance.id,
                                         created_at__isnull=False
                                         ).order_by("id").first()
    if next_instance:
        return (DAWN_OF_TIME, next_instance.created_at)
    return (DAWN_OF_TIME, datetime.now().strftime(DATETIME_FORMAT))


def _previous_created_datetime(instance, klass):
    prev_instance = klass.objects.filter(id__lt=instance.id,
                                         created_datetime__isnull=False
                                         ).order_by('-id').first()
    if prev_instance:
        return prev_instance.created_datetime.strftime(DATETIME_FORMAT)
    return DAWN_OF_TIME


def _next_created_datetime(instance, klass):
    next_instance = klass.objects.filter(id__gt=instance.id,
                                         created_datetime__isnull=False
                                         ).order_by('id').first()
    if next_instance:
        return next_instance.created_datetime.strftime(DATETIME_FORMAT)
    return datetime.now().strftime(DATETIME_FORMAT)
