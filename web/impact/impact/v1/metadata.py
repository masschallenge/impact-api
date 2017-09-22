from rest_framework.metadata import SimpleMetadata


OPTIONAL_STRING_TYPE = {"type": "string"}
OPTIONAL_BOOLEAN_TYPE = {"type": "boolean"}
OPTIONAL_DATE_TYPE = OPTIONAL_STRING_TYPE
OPTIONAL_LIST_TYPE = {"type": "field"}
OPTIONAL_ID_TYPE = {"type": "integer"}
PK_TYPE = {
    "type": "integer",
    "required": False,
    "read_only": True,
    "label": "ID"
}

READ_ONLY_LIST_TYPE = {"type": "field", "read_only": True}


class ImpactMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata["actions"] = view.METADATA_ACTIONS

        return metadata
