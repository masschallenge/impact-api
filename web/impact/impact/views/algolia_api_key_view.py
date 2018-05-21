# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from algoliasearch import algoliasearch
from django.conf import settings
from urllib.parse import urlparse
import time
from impact.permissions import DynamicModelPermissions


class AlgoliaApiKeyView(APIView):
    view_name = 'algolia_api_key_view'

    permission_classes = (
        permissions.IsAuthenticated,
        DynamicModelPermissions
    )

    actions = ["GET"]

    def get(self, request, format=None):

        client = algoliasearch.Client(
            settings.ALGOLIA_APPLICATION_ID,
            settings.ALGOLIA_API_KEY)
        params = {
            'hitsPerPage': 20,
            'filters': '',
            'validUntil': time.time() + 3600,
            'restrictIndices': ",".join(settings.ALGOLIA_INDEXES),
            'userToken': request.user.id,
            'restrictSources': urlparse(
                settings.REST_PROXY.get('HOST')).hostname
        }
        public_key = client.generateSecuredApiKey(
            settings.ALGOLIA_SEARCH_ONLY_API_KEY,
            params)
        return Response(public_key)
