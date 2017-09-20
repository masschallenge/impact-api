class ModelHelper(object):
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
        result = getattr(self, field, None)
        if result is not None:
            return result
        return getattr(self.subject, field, None)

    @classmethod
    def all_objects(cls):
        return cls.MODEL.objects.all()
