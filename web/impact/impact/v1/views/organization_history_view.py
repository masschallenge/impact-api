# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_history_view import BaseHistoryView

from accelerator.models import Organization
from impact.v1.events import (
    OrganizationBecameEntrantEvent,
    OrganizationBecameFinalistEvent,
    OrganizationBecameWinnerEvent,
    OrganizationCreatedEvent,
)


class OrganizationHistoryView(BaseHistoryView):
    view_name = "organization_history"
    model = Organization
    event_classes = [OrganizationCreatedEvent,
                     OrganizationBecameEntrantEvent,
                     OrganizationBecameFinalistEvent,
                     OrganizationBecameWinnerEvent]
