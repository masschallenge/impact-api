from abc import ABCMeta
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from impact.permissions import V1APIPermissions
from impact.v1.helpers import (
    json_object,
    json_simple_list,
)
from impact.v1.metadata import ImpactMetadata


class ImpactView(LoggingMixin, APIView):
    __metaclass__ = ABCMeta

    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata

    actions = ["GET"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def metadata(self):
        list_key = getattr(self, "list_key", "results")
        result = {}
        get = self.method_options("GET", default={})
        if "GET" in self.actions:
            result["GET"] = json_simple_list(json_object(get),
                                             list_key=list_key)
        return result

    def metadata_object_action(self, action):
        result = {}
        if action in self.actions:
            options = self.method_options(action)
            if options:
                result[action] = json_object(options)
        return result

    @classmethod
    def model(cls):
        return cls.helper_class.model

    @classmethod
    def serialize(self, obj):
        return self.helper_class(obj).serialize(self.fields().keys())

    @classmethod
    def fields(self):
        return self.helper_class.fields()

    def description_check(self, check_name):
        return check_name

    def method_options(self, method, default=False):
        result = {}
        for field, description in self.fields().items():
            options = description.get(method, default)
            if options is False:
                continue
            field_json = self._description_to_json_schema(
                description.get("json-schema", {}),
                options)
            if field_json:
                result[field] = field_json
        return result

    def _description_to_json_schema(self, json_schema, options):
        if not (self.description_check(options.get("included", True)) and
                self.description_check(options.get("allowed", True))):
            return None
        result = json_schema.copy()
        if self.description_check(options.get("required", False)):
            result["required"] = True
        description = self.description_check(options.get("description"))
        if description:
            result["description"] = description
        return result
