# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_auto_endpoint.metadata import AutoMetadataMixin
from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from .organization_detail_view import (
    organization_is_startup,
    organization_is_partner,
    public_inquiry_email,
)
from impact.serializers import GeneralSerializer
from impact.v1.metadata import ImpactMetadata
from impact.utils import parse_date
from django.db.models import Q


class OrganizationListView(APIView, AutoMetadataMixin):
    permission_classes = (
        V1APIPermissions,
    )

    metadata_class = ImpactMetadata

    serializer_class = GeneralSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = request.build_absolute_uri().split("?")[0]
        results = self._results(limit, offset)
        result = {
            "count": len(results),
            "next": _url(base_url, limit, offset + limit),
            "previous": _url(base_url, limit, offset - limit),
            "results": results,
        }
        return Response(result)

    def _results(self, limit, offset):
        queryset = Organization.objects.all()
        updated_at_gt = self.request.query_params.get('updated_at__gt', None)
        updated_at_lt = self.request.query_params.get('updated_at__lt', None)
        if updated_at_gt or updated_at_lt:
            queryset = _filter_organizations_by_date(
                queryset,
                updated_at_gt,
                updated_at_lt)
        return [serialize_org(org)
                for org in queryset[offset:offset + limit]]


def _filter_organizations_by_date(queryset, updated_at_gt, updated_at_lt):
    updated_at_gt = parse_date(updated_at_gt)
    updated_at_lt = parse_date(updated_at_lt)
    if updated_at_lt:
        queryset = queryset.filter(
            Q(updated_at__isnull=False)
        ).exclude(
            Q(updated_at__gte=updated_at_lt)
        )
    if updated_at_gt:
        queryset.filter(
            Q(updated_at__isnull=False)
        ).exclude(
            Q(updated_at__lte=updated_at_gt)
        )
    return queryset


def serialize_org(org):
    return {"id": org.id,
            "name": org.name,
            "url_slug": org.url_slug,
            "public_inquiry_email": public_inquiry_email(org),
            "is_startup": organization_is_startup(org),
            "is_partner": organization_is_partner(org),
            'updated_at': org.updated_at
            }


def _url(base_url, limit, offset):
    if offset >= 0:
        return base_url + "?limit={limit}&offset={offset}".format(
            limit=limit, offset=offset)
    return None
