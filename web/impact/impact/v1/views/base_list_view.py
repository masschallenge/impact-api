# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from rest_framework.response import Response
from django.db.models import Q

from impact.v1.helpers import (
    json_list_wrapper,
    json_object,
)
from impact.v1.views import ImpactView
from impact.utils import parse_date


class BaseListView(ImpactView):
    __metaclass__ = ABCMeta

    def metadata(self):
        result = {}
        get = self.method_options("GET", default={})
        if "GET" in self.actions:
            result["GET"] = json_list_wrapper(json_object(get))
        if "POST" in self.actions:
            post = self.method_options("POST")
            if post:
                result["POST"] = json_object(post)
        return result

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = request.build_absolute_uri().split("?")[0]
        count, results = self.results(limit, offset)
        result = {
            "count": count,
            "next": _url(base_url, limit, offset + limit),
            "previous": _url(base_url, limit, offset - limit),
            "results": results,
        }
        return Response(result)

    def results(self, limit, offset):
        queryset = self.helper_class.all_objects()
        updated_at_after = self.request.query_params.get(
            'updated_at.after', None)
        updated_at_before = self.request.query_params.get(
            'updated_at.before', None)
        if updated_at_after or updated_at_before:
            queryset = _filter_by_date(queryset,
                                       updated_at_after,
                                       updated_at_before)
        count = queryset.count()
        return (count,
                [self.serialize(obj)
                 for obj in queryset[offset:offset + limit]])


def _filter_by_date(queryset, updated_at_after, updated_at_before):
    updated_at_after = parse_date(updated_at_after)
    updated_at_before = parse_date(updated_at_before)
    if updated_at_after:
        queryset = queryset.filter(Q(updated_at__gte=updated_at_after))
    if updated_at_before:
        queryset = queryset.exclude(Q(updated_at__gt=updated_at_before))
    return queryset


def _url(base_url, limit, offset):
    if offset >= 0:
        return base_url + "?limit={limit}&offset={offset}".format(
            limit=limit, offset=offset)
    return None
