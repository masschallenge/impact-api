# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework import response, schemas
from rest_framework.decorators import (
    api_view,
    renderer_classes,
)
from drf_yasg.renderers import (
    OpenAPIRenderer,
    SwaggerUIRenderer,
)


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Impact API')
    return response.Response(generator.get_schema(request=request))
