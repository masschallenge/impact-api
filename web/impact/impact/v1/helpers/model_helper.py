from django.core.exceptions import ValidationError
from django.core.validators import (
    URLValidator,
    validate_email,
)

INVALID_BOOLEAN_ERROR = ("Invalid {field}: "
                         "Expected 'true' or 'false' not {value}")
INVALID_CHOICE_ERROR = ("Invalid {field}: "
                        "Expected {choices} not {value}")
INVALID_EMAIL_ERROR = ("Invalid {field}: "
                       "Expected '{value}' to be valid email address")
INVALID_REGEX_ERROR = "Invalid {field}: Expected '{value}' to match '{regex}'"
INVALID_STRING_ERROR = "Invalid {field}: Expected a String not {value}"
INVALID_URL_ERROR = "Invalid {field}: Expected '{value}' to be a valid URL"


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
        subject = self.subject
        # The following lines would allow a helper to
        # override the subject's setter.  We haven't
        # needed this yet, so leaving this mechanism
        # commented out.
        # attr = getattr(self.__class__, field, None)
        # if attr and attr.fset:
        #     subject = self
        setattr(subject, field, value)

    def validate(self, field, value):
        validator = self.VALIDATORS.get(field)
        if validator:
            value = validator(self, field, value)
        return value

    def save(self):
        self.subject.save()

    @classmethod
    def all_objects(cls):
        return cls.MODEL.objects.all()


def validate_boolean(helper, field, value):
    result = value
    if isinstance(result, str):
        result = result.lower()
        if result == 'true':
            result = True
        elif result == 'false':
            result = False
    if not isinstance(result, bool):
        helper.errors.append(INVALID_BOOLEAN_ERROR.format(field=field,
                                                          value=value))
    return result


def validate_string(helper, field, value):
    if not isinstance(value, str):
        helper.errors.append(INVALID_STRING_ERROR.format(field=field,
                                                         value=value))
    return value


def validate_choices(helper, field, value, choices, translations={}):
    validate_string(helper, field, value)
    result = translations.get(value, value)
    if value in choices or result in choices:
        return result
    if isinstance(result, str):
        result = translations.get(result.lower(), result)
    if result not in choices:
        helper.errors.append(INVALID_CHOICE_ERROR.format(
                field=field, value=value, choices=format_choices(choices)))
    return result


def format_choices(choices):
    choice_list = list(choices)
    if choice_list:
        result = "', '".join(choice_list[:-1])
        if result:
            result += "' or '"
        result += "%s'" % choice_list[-1]
        return "'" + result


def validate_regex(helper, field, value, regex):
    if not regex.match(value):
        helper.errors.append(INVALID_REGEX_ERROR.format(field=field,
                                                        value=value,
                                                        regex=regex.pattern))
    return value


def validate_email_address(helper, field, value):
    try:
        validate_email(value)
    except ValidationError:
        helper.errors.append(INVALID_EMAIL_ERROR.format(field=field,
                                                        value=value))
    return value


def validate_url(helper, field, value):
    try:
        URLValidator(schemes=["http", "https"])(value)
    except ValidationError:
        helper.errors.append(INVALID_URL_ERROR.format(field=field,
                                                      value=value))
    return value
