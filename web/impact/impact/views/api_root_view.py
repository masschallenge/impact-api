# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from impact.permissions import DynamicModelPermissions


User = get_user_model()


class APIRootView(APIView):
    queryset = User.objects.none()
    permission_classes = (
        permissions.IsAuthenticated,
        DynamicModelPermissions,
    )

    def get(self, request):
        urls = []
        return Response(urls)
