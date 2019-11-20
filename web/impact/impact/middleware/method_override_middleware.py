# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from django.utils.deprecation import MiddlewareMixin

METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'


class MethodOverrideMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != 'POST':
            return
        if METHOD_OVERRIDE_HEADER not in request.META:
            return
        request.method = request.META[METHOD_OVERRIDE_HEADER]
