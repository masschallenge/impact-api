# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
from pytz import utc
from django.db.models import Q
from impact.utils import (
    DAWN_OF_TIME,
    next_instance,
    previous_instance,
)
from impact.v1.events.base_history_event import BaseHistoryEvent


class OrganizationCreatedEvent(BaseHistoryEvent):
    EVENT_TYPE = "organization created"

    def __init__(self, organization):
        super().__init__()
        self.organization = organization

    @classmethod
    def events(cls, organization):
        return [cls(organization)]

    def calc_datetimes(self):
        startup = self.organization.startup_set.order_by("id").first()
        if startup:
            self._created_datetimes(startup)
            return
        partner = self.organization.partner_set.order_by("id").first()
        if partner:
            self._created_datetimes(partner)
            return
        self._created_datetimes(self.organization)

    def _created_datetimes(self, instance):
        if instance.created_at is not None:
            self.earliest = instance.created_at
        elif hasattr(instance, "created_datetime"):
            if instance.created_datetime is not None:
                self.earliest = instance.created_datetime
            else:
                self.earliest = _previous_created_datetime(instance)
                self.latest = _next_created_datetime(instance)
        else:
            query = Q(created_at__isnull=False)
            self.earliest = DAWN_OF_TIME
            previous = previous_instance(instance, query)
            if previous:
                self.earliest = previous.created_at
            self.latest = utc.localize(datetime.now())
            next = next_instance(instance, query)
            if next:
                self.latest = next.created_at


def _previous_created_datetime(instance):
    prev = previous_instance(instance,
                             Q(created_datetime__isnull=False))
    if prev:
        return prev.created_datetime
    return DAWN_OF_TIME


def _next_created_datetime(instance):
    next = next_instance(instance,
                         Q(created_datetime__isnull=False))
    if next:
        return next.created_datetime
    return datetime.now()
