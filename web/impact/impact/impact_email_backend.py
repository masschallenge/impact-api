from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend


class ImpactEmailBackend(EmailBackend):

    def send_messages(self, email_messages):
        messages = []
        if settings.SES_CONFIGURATION_SET:
            messages = self._add_logging_headers(email_messages)
        else:
            messages = email_messages
        return super().send_messages(messages)

    def _add_logging_headers(self, email_messages):
        messages = []
        for message in email_messages:
            message.extra_headers[
                'X-SES-CONFIGURATION-SET'] = settings.SES_CONFIGURATION_SET
            messages.append(message)
        return messages
