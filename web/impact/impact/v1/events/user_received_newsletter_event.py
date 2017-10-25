from django.contrib.auth import get_user_model
from impact.v1.events.base_history_event import BaseHistoryEvent
from impact.v1.helpers import (
    EMAIL_FIELD,
    STRING_FIELD,
)

User = get_user_model()


class UserReceivedNewsletterEvent(BaseHistoryEvent):
    EVENT_TYPE = "user received newsletter"
    RECEIVED_NEWSLETTER_FORMAT = "Received {name} newsletter"

    CLASS_FIELDS = {
        "newsletter_name": STRING_FIELD,
        "newsletter_from_address": EMAIL_FIELD,
    }

    def __init__(self, receipt):
        super().__init__()
        self.receipt = receipt

    @classmethod
    def events(cls, user):
        result = []
        for receipt in user.newsletterreceipt_set.all():
            result.append(cls(receipt))
        return result

    def calc_datetimes(self):
        self.earliest = (self.receipt.created_at or
                         self.receipt.newsletter.date_mailed)

    def description(self):
        return self.RECEIVED_NEWSLETTER_FORMAT.format(
            name=self.receipt.newsletter.name)

    def newsletter_name(self):
        return self.receipt.newsletter.name

    def newsletter_from_address(self):
        return self.receipt.newsletter.from_addr
