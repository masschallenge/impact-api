# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'
METHOD_OVERRIDE_HEADER = 'X-HTTP-Method-Override'

class MethodOverrideMiddleware(object):
    def process_request(self, request):
        if request.method != 'POST':
            return
        if METHOD_OVERRIDE_HEADER not in request.META:
            return
        request.method = request.META[METHOD_OVERRIDE_HEADER]
