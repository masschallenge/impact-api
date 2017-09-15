class ModelHelper(object):
    KEY_TRANSLATIONS = {}

    def __init__(self, subject):
        self.subject = subject

    def serialize(self):
        result = {}
        for field in self.OUTPUT_KEYS:
            value = self.field_value(field)
            if value is not None:
                result[field] = value
        return result

    def field_value(self, field):
        return getattr(self.subject, self.translate(field))

    @classmethod
    def translate(cls, field):
        return cls.KEY_TRANSLATIONS.get(field, field)
