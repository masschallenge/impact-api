from abc import (
    ABCMeta,
    abstractmethod,
)
from impact.v1.helpers import (
    STRING_FIELD,
)


class BaseHistoryEvent(object):
    __metaclass__ = ABCMeta

    CLASS_FIELDS = {
        "event_type": STRING_FIELD,
        "datetime": STRING_FIELD,
        "latest_datetime": STRING_FIELD,
        "description": STRING_FIELD,
    }

    def __init__(self):
        self.earliest = None
        self.latest = None

    @classmethod
    def all_fields(cls):
        result = {}
        for base_class in cls.__bases__:
            if hasattr(base_class, "all_fields"):
                result.update(base_class.all_fields())
        if hasattr(cls, "CLASS_FIELDS"):
            result.update(cls.CLASS_FIELDS)
        return result

    @classmethod
    def event_type(cls):
        return cls.EVENT_TYPE

    @abstractmethod
    def calc_datetimes(self):
        pass  # pragma: no cover

    def datetime(self):
        self._check_date_cache()
        return self.earliest

    def latest_datetime(self):
        self._check_date_cache()
        return self.latest

    def _check_date_cache(self):
        if not self.earliest and hasattr(self, "calc_datetimes"):
            self.calc_datetimes()

    def description(self):
        return None  # pragma: no cover

    def serialize(self):
        result = {}
        for key in self.all_fields().keys():
            value = getattr(self, key)()
            if value is not None:
                result[key] = value
        return result
