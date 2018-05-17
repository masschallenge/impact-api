# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from rest_framework.views import APIView
from rest_framework.response import Response
from impact.permissions import V1APIPermissions
from impact.v1.helpers import (
    json_object,
    json_simple_list,
)
from impact.v1.metadata import ImpactMetadata
from algoliasearch import algoliasearch
from django.conf import settings
import time


class AlgoliaApiKeyView(APIView):
    view_name = 'algolia_api_key_view'

    permission_classes = (
        
    )

    actions = ["GET"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def get(self, request, format=None):

        client = algoliasearch.Client(
            settings.ALGOLIA_APPLICATION_ID,
            settings.ALGOLIA_API_KEY)
        params = {
            'hitsPerPage': 20,
            'filters': '_tags:user_42 AND available = 1',
            'validUntil': time.time() + 3600,
            'restrictIndices': 'index1,index2',
            'userToken': 'user_42',
            'restrictSources': '192.168.1.0/24'
        }
        public_key = client.generateSecuredApiKey(
            settings.ALGOLIA_SEARCH_ONLY_API_KEY,
            params)
        return Response([public_key])


