# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings

from rest_framework.response import Response
from rest_framework_proxy.views import ProxyView

from impact.permissions import (
    V0APIPermissions,
)


class MentorsProxyView(ProxyView):
    source = 'api/mentors/'
    verify_ssl = False
    permission_classes = (
        V0APIPermissions,
    )

    def post(self, *args, **kwargs):
        if not self.valid(self.request.POST):
            return Response(status=404, data=self.errors)
        self.request.POST._mutable = True
        self.request.POST['SiteName'] = settings.V0_SITE_NAME
        self.request.POST['SecurityKey'] = settings.V0_SECURITY_KEY
        self.request.POST._mutable = False
        self.request.query_params._mutable = True
        self.request.query_params['SiteName'] = settings.V0_SITE_NAME
        self.request.query_params['SecurityKey'] = settings.V0_SECURITY_KEY
        self.request.query_params._mutable = False
        self.log()
        return self.proxy(self.request, *args, **kwargs)

    def valid(self, data):
        self.errors = []
        if "SiteName" in data:
            self.errors.append("SiteName is deprecated")
        if not settings.V0_SITE_NAME:
            self.errors.append("Default SiteName is not set")
        if "SecurityKey" in data:
            self.errors.append("SecurityKey is deprecated")
        if not settings.V0_SECURITY_KEY:
            self.errors.append("Default SecurityKey is not set")
        return self.errors == []
