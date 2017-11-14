# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_tracking.mixins import LoggingMixin

from impact.models.utils import snake_to_camel_case
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
        if self.kwargs['model'] in model_attribute_calls:
            return apps.get_model(
                app_label=self.kwargs['app'],
                model_name=self.kwargs['model'])
        else:
            return apps.get_model(
                app_label=self.kwargs['app'],
                model_name=snake_to_camel_case(self.kwargs['model']))


    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer
