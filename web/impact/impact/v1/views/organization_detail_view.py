# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    Organization,
    Partner,
    Startup,
)

INVALID_KEYS_ERROR = ("Received invalid key(s): {invalid_keys}. "
                      "Valid keys are: {valid_keys}.")


def organization_is_startup(organization):
    return _organization_is(organization, Startup)


def organization_is_partner(organization):
    return _organization_is(organization, Partner)


def public_inquiry_email(organization):
    for klass in (Partner, Startup):
        qs = klass.objects.filter(organization=organization)
        if qs.exists():
            return qs.first().public_inquiry_email
    return ""


def _organization_is(organization, klass):
    return klass.objects.filter(organization=organization).exists()


class OrganizationDetailView(APIView):
    model = Organization
    model_fields = ["name", "url_slug"]
    derived_field_functions = {"public_inquiry_email": public_inquiry_email,
                               "is_startup": organization_is_startup,
                               "is_partner": organization_is_partner}

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        result = self.get_model_fields()
        result.update(self.derived_fields())
        return Response(result)

    def get_model_fields(self):
        return {field: getattr(self.instance, field)
                for field in self.model_fields}

    def derived_fields(self):
        return {key: func(self.instance)
                for (key, func) in self.derived_field_functions.items()}
