# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_history_view import BaseHistoryView

from impact.models import Organization
from impact.v1.events import (
    OrganizationBecomeEntrantEvent,
    OrganizationBecomeFinalistEvent,
    OrganizationCreatedEvent,
)


class OrganizationHistoryView(BaseHistoryView):
    model = Organization
    event_classes = [OrganizationCreatedEvent,
                     OrganizationBecomeEntrantEvent,
                     OrganizationBecomeFinalistEvent]