# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import magic

from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework_proxy.views import ProxyView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V0APIPermissions
)
from impact.v0.views.utils import encrypt_image_token


class ImageProxyView(LoggingMixin, ProxyView):
    source = "api/image/"
    verify_ssl = False
    return_raw = True
    permission_classes = (
        V0APIPermissions,
    )

    def create_response(self, response):
        magic.Magic(mime=True)
        ctype = magic.from_buffer(response.content, mime=True)
        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=ctype)

    def get(self, *args, **kwargs):
        if not self.valid(self.request.GET):
            return Response(status=404, data=self.errors)
        self.request.GET = self.request.GET.copy()
        self._update_get_parameter("Size",
                                   self.request.GET.get("Size", "100x100"))
        self._update_get_parameter("SiteName", settings.V0_SITE_NAME)
        self._update_get_parameter("ImageToken", self._secure_image_token())
        return self.proxy(self.request, *args, **kwargs)

    def valid(self, data):
        self.errors = []
        if "ImageToken" not in data or not data["ImageToken"]:
            self.errors.append("ImageToken not found")
        if "SiteName" in data:
            self.errors.append("SiteName is deprecated")
        if not settings.V0_SITE_NAME:
            self.errors.append("Default SiteName is not set")
        return self.errors == []

    def _update_get_parameter(self, param, value):
        self.request.GET[param] = value
        self.request.query_params._mutable = True
        self.request.query_params[param] = value
        self.request.query_params._mutable = False

    def _secure_image_token(self):
        image_token = encrypt_image_token(self.request.GET["ImageToken"],
                                          settings.V0_SECURITY_KEY)
        return image_token + b"="
