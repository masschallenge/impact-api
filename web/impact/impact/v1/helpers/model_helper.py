class ModelHelper(object):
    VALIDATORS = {}

    def __init__(self, subject):
        self.subject = subject
        self.errors = []

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
        attr = getattr(self.__class__, field, None)
        if attr and attr.fset:
            setattr(self, field, value)
        else:
            setattr(self.subject, field, value)

    def validate(self, field, value):
        validator = self.VALIDATORS.get(field)
        if validator:
            return validator(self, value)
        return value

    def save(self):
        self.subject.save()

    @classmethod
    def all_objects(cls):
        return cls.MODEL.objects.all()
