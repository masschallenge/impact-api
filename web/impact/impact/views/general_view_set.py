# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps

from rest_framework import viewsets
from rest_framework import permissions

from ..model_utils import snake_to_model_name
from ..permissions import DynamicModelPermissions
from ..serializers import GeneralSerializer
from ..utils import model_name_case


MODELS_TO_EXCLUDE_FROM_URL_BINDING = ["JobPosting"]


class GeneralViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        DynamicModelPermissions,
    )

    @property
    def model(self): 
        model = snake_to_model_name(self.kwargs.get('model', ''))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.hellooooooooooo", model)
        related_model = self.kwargs.get('related_model', '')
        print("*******************************.hellooooooooooo", self.kwargs)
        model_name = model_name_case(model, related_model)
        model = apps.get_model(
            app_label=self.kwargs['app'],
            model_name=model_name)
        if model.__name__ in MODELS_TO_EXCLUDE_FROM_URL_BINDING:
            raise LookupError("'%s' is not available=============" % (model_name))
        return model

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer
