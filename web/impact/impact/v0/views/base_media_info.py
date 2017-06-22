# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.sites.models import Site


class BaseMediaInfo(object):
    _url = None

    @classmethod
    def url(cls, suffix=""):
        if cls._url:
            return cls._url + suffix
        cls._url = "http://" + Site.objects.get_current().domain + "/media/"
        return cls._url + suffix
