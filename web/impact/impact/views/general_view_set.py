# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_tracking.mixins import LoggingMixin

from impact.models.utils import snake_to_model_name
from impact.permissions import DynamicModelPermissions
from impact.serializers import GeneralSerializer


model_attribute_calls = [
    'Startup_additional_industries',
    'Startup_recommendation_tags',
    'StartupLabel_startups',
    'RefundCode_programs',
    'UserLabel_users',
    'Observer_newsletter_cc_roles',
    'ExpertProfile_functional_expertise',
    'ExpertProfile_additional_industries',
    'ExpertProfile_mentoring_specialties',
    'Newsletter_recipient_roles',
    'Section_interest_categories',
]


class GeneralViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        DynamicModelPermissions,
    )

    @property
    def model(self):
        model = snake_to_model_name(self.kwargs['model'])
        related_model = self.kwargs.get('related_model')

        if related_model:
            model_name = model + '_' + related_model
        else:
            model_name = model

        return apps.get_model(
            app_label=self.kwargs['app'],
            model_name=model_name)

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer
