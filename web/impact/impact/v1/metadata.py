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
        metadata["actions"] = view.metadata()
        return metadata
