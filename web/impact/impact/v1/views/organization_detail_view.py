from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.utils import (
    ALL_USER_RELATED_KEYS,
    INVALID_GENDER_ERROR,
    PROFILE_KEYS,
    USER_KEYS,
    KEY_TRANSLATIONS,
    find_gender,
    get_profile,
    user_gender,
)

INVALID_KEYS_ERROR = ("Received invalid key(s): {invalid_keys}. "
                      "Valid keys are: {valid_keys}.")




class OrganizationDetailView(APIView):
    model = Organization
    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):

        instance = self.model.objects.get(pk=pk)        
        fields = ["name", "url_slug",]
        result = {
            field: getattr(instance, field) for field in fields}
        return Response(result)

