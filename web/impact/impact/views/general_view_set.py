# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_tracking.mixins import LoggingMixin

from impact.models.utils import snake_to_camel_case
from impact.permissions import DynamicModelPermissions
from impact.serializers import GeneralSerializer


class GeneralViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        DynamicModelPermissions,
    )

    @property
    def model(self):
        return apps.get_model(
            app_label=self.kwargs['app'],
            model_name=snake_to_camel_case(self.kwargs['model']))

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer
