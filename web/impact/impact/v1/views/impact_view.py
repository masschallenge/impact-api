from abc import (
    ABCMeta,
    abstractmethod,
)
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin


def _json_object(properties):
    return {
        "type": "object",
        "properties": properties,
    }


def _json_array(item):
    return {
        "type": "array",
        "item": item,
    }


class ImpactView(LoggingMixin, APIView):
    __metaclass__ = ABCMeta

    @abstractmethod
    def metadata(self):
        pass  # pragma: no cover

    def description_check(self, check_name):
        return check_name

    def options_from_fields(self, fields, actions):
        result = {}
        get = self._method_options("GET", fields, default={})
        if "GET" in actions:
            result["GET"] = _json_object(get)
        if "GET_LIST" in actions:
            result["GET"] = _json_array(_json_object(get))
        if "PATCH" in actions:
            patch = self._method_options("PATCH", fields)
            if patch:
                result["PATCH"] = _json_object(patch)
        if "POST" in actions:
            post = self._method_options("POST", fields)
            if post:
                result["POST"] = _json_object(post)
        return result

    def _method_options(self, method, fields, default=False):
        result = {}
        for field, description in fields.items():
            options = description.get(method, default)
            if options is False:
                continue
            field_json = self._description_to_json_schema(
                description.get("json-schema", {}),
                options)
            if field_json:
                result[field] = field_json
        return result

    def _description_to_json_schema(self, json_schema, method_options):
        if not (self.description_check(
                    method_options.get("included", True)) and
                self.description_check(
                    method_options.get("allowed", True))):
            return None
        result = json_schema.copy()
        if self.description_check(method_options.get("required", False)):
            result["required"] = True
        description = self.description_check(method_options.get("description"))
        if description:
            result["description"] = description
        return result
