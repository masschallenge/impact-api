from django.contrib.auth import get_user_model

User = get_user_model()


class UserReceivedNewsletterEvent(object):
    EVENT_TYPE = "user received newsletter"
    RECEIVED_NEWSLETTER_FORMAT = "Received {name} newsletter"

    def __init__(self, receipt):
        self.receipt = receipt

    @classmethod
    def events(cls, user):
        result = []
        for receipt in user.newsletterreceipt_set.all():
            result.append(cls(receipt))
        return result

    def serialize(self):
        return {
            "datetime": self._datetime(),
            "event_type": self.EVENT_TYPE,
            "description": self.RECEIVED_NEWSLETTER_FORMAT.format(
                name=self.receipt.newsletter.name),
            "newsletter_name": self.receipt.newsletter.name,
            "newsletter_from_address": self.receipt.newsletter.from_addr,
            }

    def _datetime(self):
        return self.receipt.created_at or self.receipt.newsletter.date_mailed
