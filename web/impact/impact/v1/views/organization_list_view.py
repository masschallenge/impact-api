# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.utils import (
    find_gender,
    user_gender,
    ALL_USER_RELATED_KEYS,
    INVALID_GENDER_ERROR,
    KEY_TRANSLATIONS,
    PROFILE_KEYS,
    REQUIRED_PROFILE_KEYS,
    REQUIRED_USER_KEYS,
    USER_KEYS,
)


class OrganizationListView(APIView):
    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = request.build_absolute_uri().split("?")[0]
        result = {
            "count": Organization.objects.count(),
            "next": _url(base_url, limit, offset + limit),
            "previous": _url(base_url, limit, offset - limit),
            "results": _results(limit, offset),
            }
        return Response(result)

    def post(self, request):
        return Response({"foo": "bar"})                        

def _results(limit, offset):
    return [_serialize_org(org)
            for org in Organization.objects.all()[offset:offset+limit]]
                        

def _serialize_org(org):
    return {"id": org.id,
            "name": org.name}
                        
def _url(base_url, limit, offset):
    if offset >= 0:
        return base_url + "?limit={limit}&offset={offset}".format(
            limit=limit, offset=offset)
    return None
