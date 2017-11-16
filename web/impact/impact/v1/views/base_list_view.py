# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from urllib.parse import (
    parse_qs,
    urlunparse,
    urlencode,
    urlparse,
)

from rest_framework.response import Response

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
        result.update(self.metadata_object_action("POST"))
        return result

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = _base_url(request)
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
        queryset = self.filter(queryset)
        count = queryset.count()
        return (count,
                [self.serialize(obj)
                 for obj in queryset[offset:offset + limit]])

    def filter(self, queryset):
        updated_at_after = self.request.query_params.get(
            'updated_at.after', None)
        updated_at_before = self.request.query_params.get(
            'updated_at.before', None)
        if updated_at_after or updated_at_before:
            queryset = self._filter_by_date(queryset,
                                            updated_at_after,
                                            updated_at_before)
        return queryset

    def _filter_by_date(self, qs, after, before):
        updated_at_after = parse_date(after)
        updated_at_before = parse_date(before)
        if updated_at_after:
            qs = qs.filter(updated_at__gte=updated_at_after)
        if updated_at_before:
            qs = qs.exclude(updated_at__gt=updated_at_before)
        return qs


def _url(base_url, limit, offset):
    if offset >= 0:
        url = _update_query_param(base_url, "limit", limit)
        url = _update_query_param(url, "offset", offset)
        return url
    return None


def _base_url(request):
    absolute_uri = request.build_absolute_uri()
    absolute_uri = _remove_query_param(absolute_uri, "offset")
    absolute_uri = _remove_query_param(absolute_uri, "limit")
    return absolute_uri


def _remove_query_param(url, query_param_key):
    parsed = urlparse(url)
    qs = parsed.query
    if not qs:
        return url
    parsed_qs = parse_qs(qs, strict_parsing=True)
    parsed_qs.pop(query_param_key, None)
    return _build_url_with_query(parsed, parsed_qs)


def _update_query_param(url, query_param_key, query_param_value=None):
    parsed = urlparse(url)
    qs = parsed.query
    parsed_qs = parse_qs(qs) if qs else {}
    parsed_qs.update({query_param_key: query_param_value})
    return _build_url_with_query(parsed, parsed_qs)


def _build_url_with_query(parsed_url, parsed_qs):
    return urlunparse((parsed_url[0],
                       parsed_url[1],
                       parsed_url[2],
                       parsed_url[3],
                       urlencode(parsed_qs, doseq=True),
                       parsed_url[5]))
