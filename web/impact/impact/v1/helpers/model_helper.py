class ModelHelper(object):
    def __init__(self, subject):
        self.subject = subject

    def serialize(self, fields=None):
        fields = fields or self.OUTPUT_KEYS
        result = {}
        for field in fields:
            value = self.field_value(field)
            if value is not None:
                result[field] = value
        return result

    def field_value(self, field):
        result = getattr(self, field, None)
        if result is not None:
            return result
        return getattr(self.subject, field, None)

    def field_setter(self, field, value):
        if getattr(self, field).fset:
            return value
        return getattr(self.subject, field, None)

    @classmethod
    def all_objects(cls):
        return cls.MODEL.objects.all()
