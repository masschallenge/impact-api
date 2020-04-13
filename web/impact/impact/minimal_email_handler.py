from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class MinimalEmailHandler:
    '''
    A simplistic outgoing email handler, to consolidate outgoing
    mail sending needs of impact-api calls
    attachment, if any, should be a triple of (filename, content, filetype)
    attach_alternative, if any, should be a tuple of (attachment_text, MIME_type)
      (generally used for html version of the email)
    '''
    def __init__(self,
                 to,
                 subject,
                 body,
                 from_email=None,
                 bcc=None,
                 attachment=None,
                 attach_alternative=None):
        self.email = EmailMultiAlternatives(
            subject,
            body,
            to=to,
            bcc=bcc or [settings.BCC_EMAIL],
            from_email = from_email or [settings.NO_REPLY_EMAIL])
        if attachment:
            self.email.attach(*attachment)
        if attach_alternative:
            self.email.attach_alternative(*attach_alternative)
    
    def send(self):
        self.email.send()
        
            
