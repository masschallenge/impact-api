# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm


class ImpactUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = get_user_model()
