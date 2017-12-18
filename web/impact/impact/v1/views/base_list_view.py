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
from impact.models.utils import model_has_field

VALUE_OF_LIMIT_NOT_INTEGER_ERROR = "value of 'limit' should be an integer"
GREATER_THAN_MAX_LIMIT_ERROR = "maximum allowed value for 'limit' is {}"

DEFAULT_MAX_LIMIT = 200


class BaseListView(ImpactView):
    __metaclass__ = ABCMeta
    MAX_LIMIT = DEFAULT_MAX_LIMIT
    DEFAULT_LIMIT = '10'

    def metadata(self):
        result = {}
        get = self.method_options("GET", default={})
        if "GET" in self.actions:
            result["GET"] = json_list_wrapper(json_object(get))
        result.update(self.metadata_object_action("POST"))
        return result

    def get(self, request):
        limit = self._validate_limit(
            request.GET.get('limit', self.DEFAULT_LIMIT))
        if self.errors:
            return Response(status=401, data=self.errors)
        offset = int(request.GET.get('offset', 0))
        base_url = _base_url(request)
        count, results = self.results(limit, offset)
        result = {
            "count": count,
            "next": _next_url(base_url, limit, offset, count),
            "previous": _previous_url(base_url, limit, offset, count),
            "results": results,
        }
        return Response(result)

    def _validate_limit(self, limit):
        if not limit.isdigit():
            self.errors.append(VALUE_OF_LIMIT_NOT_INTEGER_ERROR)
            limit = self.DEFAULT_LIMIT
        elif int(limit) > self.MAX_LIMIT:
            self.errors.append(
                GREATER_THAN_MAX_LIMIT_ERROR.format(self.MAX_LIMIT))
        return int(limit)

    def results(self, limit, offset):
        queryset = self.helper_class.all_objects()
        queryset = self.filter(queryset)
        count = queryset.count()
        return (count,
                [self.serialize(obj)
                 for obj in queryset[offset:offset + limit]])

    def filter(self, qs):
        qs = self._filter_by_date(qs)
        if model_has_field(self.model(), "name"):
            qs = self._filter_by_name(qs)
        return qs

    def _filter_by_date(self, qs):
        updated_at_after = self.request.query_params.get(
            'updated_at.after', None)
        updated_at_before = self.request.query_params.get(
            'updated_at.before', None)
        if updated_at_after or updated_at_before:
            qs = self._apply_filter_by_date(qs,
                                            updated_at_after,
                                            updated_at_before)
        return qs

    def _apply_filter_by_date(self, qs, after, before):
        updated_at_after = parse_date(after)
        updated_at_before = parse_date(before)
        if updated_at_after:
            qs = qs.filter(updated_at__gte=updated_at_after)
        if updated_at_before:
            qs = qs.exclude(updated_at__gt=updated_at_before)
        return qs

    def _filter_by_name(self, qs):
        name_filter = self.request.query_params.get('name', None)
        if name_filter:
            return qs.filter(name__icontains=name_filter)
        return qs


def _previous_url(base_url, limit, offset, count):
    if offset == 0:
        return None
    elif 0 <= offset < limit:
        url = _update_query_param(base_url, "limit", limit)
        return url
    else:
        url = _update_query_param(base_url, "limit", limit)
        url = _update_query_param(url, "offset", min(offset, count) - limit)
        return url
    # todo: refactor


def _next_url(base_url, limit, offset, count):
    if offset + limit >= count:
        return None
    if offset >= 0:
        url = _update_query_param(base_url, "limit", limit)
        url = _update_query_param(url, "offset", offset + limit)
        return url
    # todo: refactor
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
