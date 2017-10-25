from rest_framework.metadata import SimpleMetadata


class ImpactMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata["actions"] = view.metadata()
        return metadata
