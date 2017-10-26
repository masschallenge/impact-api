# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from drf_auto_endpoint.metadata import AutoMetadataMixin
from impact.v1.views.base_list_view import BaseListView


class ListView(BaseListView, AutoMetadataMixin):
    __metaclass__ = ABCMeta
