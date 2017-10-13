# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

METHOD_OVERRIDE_HEADER = 'X-HTTP-Method-Override'


class MethodOverrideMiddleware(object):
    def process_request(self, request):
        if request.method != 'POST':
            return
        try:
            request.META['headers']
            if METHOD_OVERRIDE_HEADER not in request.META['headers']:
                return
            request.method = request.META['headers'][METHOD_OVERRIDE_HEADER]
        except KeyError:
            return
