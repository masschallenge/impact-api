from abc import (
    ABCMeta,
    # abstractmethod,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from impact.v1.helpers import (
    json_list_wrapper,
    json_object,
    json_simple_list,
)


class ImpactView(LoggingMixin, APIView):
    __metaclass__ = ABCMeta

#     @abstractmethod
#     def actions(self):
#         pass  # pragma: no cover

#     @abstractmethod
#     def fields(self):
#         pass  # pragma: no cover

    def metadata(self):
        return self.options_from_fields(self.fields(), self.actions())

    @classmethod
    def model(cls):
        return cls.helper_class.model

    def get(self, request, pk):
        if "GET" in self.actions():
            self.instance = self.model().objects.get(pk=pk)
            return Response(self.helper_class(self.instance).serialize(
                    self.fields().keys()))

    @classmethod
    def fields(self):
        return self.helper_class.fields()

    @classmethod
    def actions(self):
        return ["GET"]

    def description_check(self, check_name):
        return check_name

    def options_from_fields(self, fields, actions, key="results"):
        result = {}
        get = self._method_options("GET", fields, default={})
        if "GET" in actions:
            result["GET"] = json_object(get)
        if "GET_LIST" in actions:
            result["GET"] = json_list_wrapper(json_object(get))
        if "SIMPLE_LIST" in actions:
            result["GET"] = json_simple_list(json_object(get), key=key)
        if "PATCH" in actions:
            patch = self._method_options("PATCH", fields)
            if patch:
                result["PATCH"] = json_object(patch)
        if "POST" in actions:
            post = self._method_options("POST", fields)
            if post:
                result["POST"] = json_object(post)
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
