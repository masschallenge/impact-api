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
            metadata["actions"] = options_from_fields(view, view.FIELDS)
        else:
            metadata["actions"] = view.METADATA_ACTIONS
        return metadata


def options_from_fields(view, fields):
    result = {}
    result["GET"] = _method_options(view, "GET", fields, default={})
    patch = _method_options(view, "PATCH", fields)
    if patch:
        result["PATCH"] = patch
    post = _method_options(view, "POST", fields)
    if post:
        result["POST"] = post
    return result


def _method_options(view, method, fields, default=False):
    result = {}
    for field, description in fields.items():
        options = description.get(method, default)
        if options is False:
            continue
        field_json = _description_to_json_schema(
            view,
            description.get("json-schema", {}),
            options)
        if field_json:
            result[field] = field_json
    return result


def _description_to_json_schema(view, json_schema, method_options):
    if not (view.description_check(method_options.get("included", True)) or
            view.description_check(method_options.get("allowed", True))):
        return None
    result = json_schema.copy()
    if view.description_check(method_options.get("required", False)):
        result["required"] = True
    description = view.description_check(method_options.get("description"))
    if description:
        result["description"] = description
    return result
