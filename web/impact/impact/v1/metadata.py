from rest_framework.metadata import SimpleMetadata


OPTIONAL_BOOLEAN_TYPE = {"type": "boolean"}
OPTIONAL_ID_TYPE = {"type": "integer"}
OPTIONAL_LIST_TYPE = {"type": "field"}
OPTIONAL_STRING_TYPE = {"type": "string"}
OPTIONAL_DATE_TYPE = OPTIONAL_STRING_TYPE
PK_TYPE = {
    "type": "integer",
    "required": False,
    "read_only": True,
    "label": "ID"
}

READ_ONLY_LIST_TYPE = {"type": "field", "read_only": True}
READ_ONLY_STRING_TYPE = {"type": "string", "read_only": True}


class ImpactMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        if hasattr(view, "FIELDS"):
            metadata["actions"] = options_from_fields(view.FIELDS, request)
        else:
            metadata["actions"] = view.METADATA_ACTIONS

        return metadata


def options_from_fields(fields, request):
    result = {}
    result["GET"] = _method_options("GET", fields, request, default={})
    patch = _method_options("PATCH", fields, request)
    if patch:
        result["PATCH"] = patch
    post = _method_options("POST", fields, request)
    if post:
        result["POST"] = post
    return result


def _method_options(method, fields, request, default=False):
    result = {}
    for field, description in fields.items():
        options = description.get(method, default)
        if options is False:
            continue
        field_json = _description_to_json_schema(
            description.get("json-schema", {}),
            options,
            request)
        if field_json:
            result[field] = field_json
    return result


def _description_to_json_schema(json_schema, method_options, request):
    if not (_method_check(method_options.get("included", True), request) or
            _method_check(method_options.get("allowed", True), request)):
        return None
    result = json_schema.copy()
    if _method_check(method_options.get("required", False), request):
        result["required"] = True
    description = _method_check(method_options.get("description"), request)
    if description:
        result["description"] = description
    return result


def _method_check(method, request):
    if callable(method):
        return method(request)
    return method
