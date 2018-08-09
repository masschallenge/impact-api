# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class JWTCookieNameView(APIView):
    view_name = 'jwt_cookie_name_view'

    permission_classes = (
        permissions.IsAuthenticated,
    )

    actions = ["GET"]

    def get(self, request, format=None):
        return Response({'name': settings.JWT_AUTH.get('JWT_AUTH_COOKIE')})
