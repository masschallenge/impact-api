# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class IndexView(View):

    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return HttpResponseRedirect(reverse('api-root'))
        return render(request, self.template_name, {})
