class ModelHelper(object):
    KEY_TRANSLATIONS = {}

    def serialize(self):
        result = {}
        for field in self.OUTPUT_KEYS:
            result[field] = getattr(self.subject, self.translate(field))
        return result

    @classmethod
    def translate(cls, field):
        return cls.KEY_TRANSLATIONS.get(field, field)
