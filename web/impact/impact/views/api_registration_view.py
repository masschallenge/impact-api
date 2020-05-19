# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.urls import reverse
from django_registration.backends.one_step.views import RegistrationView


class APIRegistrationView(RegistrationView):

    def get_success_url(self, user):
        return reverse('api-root')
