from datetime import datetime
from pytz import utc
from impact.models import (
    Organization,
    Partner,
    Startup,
)
from impact.utils import DAWN_OF_TIME


class OrganizationCreatedEvent(object):
    EVENT_TYPE = "organization created"

    def __init__(self, organization):
        self.organization = organization

    @classmethod
    def events(cls, organization):
        return [cls(organization)]

    def serialize(self):
        earliest, latest = self._created_datetime()
        return {
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": self.EVENT_TYPE,
            "description": "",
            }

    def _created_datetime(self):
        startup = self.organization.startup_set.order_by("id").first()
        if startup:
            return _created_datetimes(startup, Startup)
        partner = self.organization.partner_set.order_by("id").first()
        if partner:
            return _created_datetimes(partner, Partner)
        return _created_datetimes(self.organization, Organization)


def _created_datetimes(instance, cls):
    if instance.created_at is not None:
        return (instance.created_at, instance.created_at)
    if hasattr(instance, "created_datetime"):
        if instance.created_datetime is not None:
            return (instance.created_datetime,
                    instance.created_datetime)
        return (_previous_created_datetime(instance, cls),
                _next_created_datetime(instance, cls))
    next_instance = cls.objects.filter(id__gt=instance.id,
                                       created_at__isnull=False
                                       ).order_by("id").first()
    if next_instance:
        return (DAWN_OF_TIME, next_instance.created_at)
    return (DAWN_OF_TIME, utc.localize(datetime.now()))


def _previous_created_datetime(instance, cls):
    prev_instance = cls.objects.filter(id__lt=instance.id,
                                       created_datetime__isnull=False
                                       ).order_by('-id').first()
    if prev_instance:
        return prev_instance.created_datetime
    return DAWN_OF_TIME


def _next_created_datetime(instance, cls):
    next_instance = cls.objects.filter(id__gt=instance.id,
                                       created_datetime__isnull=False
                                       ).order_by('id').first()
    if next_instance:
        return next_instance.created_datetime
    return datetime.now()
