from django.core.exceptions import ValidationError
from django.core.validators import (
    URLValidator,
    validate_email,
)
INVALID_BOOLEAN_ERROR = ("Invalid {field}: "
                         "Expected 'true' or 'false' not {value}")
INVALID_INTEGER_ERROR = ("Invalid {field}: "
                         "Expected integer not {value}")
INVALID_FLOAT_ERROR = ("Invalid {field}: "
                       "Expected floating-point number not {value}")

INVALID_CHOICE_ERROR = ("Invalid {field}: "
                        "Expected {choices} not {value}")
INVALID_EMAIL_ERROR = ("Invalid {field}: "
                       "Expected '{value}' to be valid email address")
INVALID_REGEX_ERROR = "Invalid {field}: Expected '{value}' to match '{regex}'"
INVALID_STRING_ERROR = "Invalid {field}: Expected a String not {value}"
INVALID_URL_ERROR = "Invalid {field}: Expected '{value}' to be a valid URL"


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


def _make_validator(cls, error_msg):
    def validate_cls(helper, field, value):
        try:
            result = cls(value)
        except ValueError:
            helper.errors.append(error_msg.format(field=field,
                                                  value=value))
        return result


validate_float = _make_validator(float, INVALID_FLOAT_ERROR)
validate_integer = _make_validator(int, INVALID_INTEGER_ERROR)


def validate_choices(helper, field, value, choices):
    validate_string(helper, field, value)
    if value not in choices:
        helper.errors.append(INVALID_CHOICE_ERROR.format(
            field=field, value=value, choices=format_choices(choices)))
    return value


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
    if value:
        try:
            URLValidator(schemes=["http", "https"])(value)
        except ValidationError:
            helper.errors.append(INVALID_URL_ERROR.format(field=field,
                                                          value=value))
    return value
