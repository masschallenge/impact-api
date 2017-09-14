class OrganizationHelper(object):
    def __init__(self, organization):
        self.org = organization

    def serialize(self):
        return {
            "id": self.org.id,
            "name": self.org.name,
            "url_slug": self.org.url_slug,
            "public_inquiry_email": self.org.public_inquiry_email,
            "is_startup": self.is_startup(),
            "is_partner": self.is_partner(),
            'updated_at': self.org.updated_at
            }

    def is_startup(self):
        return self.org.startup_set.exists()

    def is_partner(self):
        return self.org.partner_set.exists()
