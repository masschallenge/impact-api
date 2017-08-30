# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_history_view import BaseHistoryView

from impact.models import Organization
from impact.v1.events import (
    OrganizationBecameEntrantEvent,
    OrganizationBecameFinalistEvent,
    OrganizationCreatedEvent,
)


class OrganizationHistoryView(BaseHistoryView):
    model = Organization
    event_classes = [OrganizationCreatedEvent,
                     OrganizationBecameEntrantEvent,
                     OrganizationBecameFinalistEvent]
