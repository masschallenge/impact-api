# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps
from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from drf_auto_endpoint.router import router as schema_router
from impact.graphql.utils.custom_error_view import SafeGraphQLView
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from impact.graphql.middleware import IsAuthenticatedMiddleware
from impact.graphql.schema import (
    auth_schema,
    schema,
)
from impact.model_utils import model_name_to_snake
from impact.schema import schema_view
from impact.v0.urls import v0_urlpatterns
from impact.v1.urls import v1_urlpatterns
from impact.views import (
    AlgoliaApiKeyView,
    GeneralViewSet,
    IndexView,
    JWTCookieNameView,
)
from .views.general_view_set import MODELS_TO_EXCLUDE_FROM_URL_BINDING

accelerator_router = routers.DefaultRouter()
simpleuser_router = routers.DefaultRouter()
simpleuser_router.register('User', GeneralViewSet, base_name='User')

for model in apps.get_models('accelerator'):
    if (model._meta.app_label == 'accelerator' and not
            model._meta.auto_created and
            model.__name__ not in MODELS_TO_EXCLUDE_FROM_URL_BINDING):
        schema_router.register(
            model, url=model_name_to_snake(model.__name__))

sso_urlpatterns = [
    url(r'^obtain-token/', obtain_jwt_token),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^verify-token/', verify_jwt_token),
]

account_urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
]

urls = [
    url(r'^api/sso/token_name/', JWTCookieNameView.as_view(),
        name=JWTCookieNameView.view_name),
    url(r'^api/algolia/api_key/$', AlgoliaApiKeyView.as_view(),
        name=AlgoliaApiKeyView.view_name),
    url(r'^api/v0/', include(v0_urlpatterns)),
    url(r'^api/v1/', include(v1_urlpatterns)),
    url(r'^api/(?P<app>\w+)/(?P<model>[a-z_]+)/'
        r'(?P<related_model>[a-z_]+)/$',
        GeneralViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='related-object-list'),
    url(r'^api/(?P<app>\w+)/(?P<model>[a-z_]+)/'
        r'(?P<related_model>[a-z_]+)/'
        r'(?P<pk>[0-9]+)/$',
        GeneralViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='related-object-detail'),
    url(r'^api/(?P<app>\w+)/(?P<model>[a-z_]+)/$',
        GeneralViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='object-list'),
    url(r'^api/(?P<app>\w+)/(?P<model>[a-z_]+)/(?P<pk>[0-9]+)/$',
        GeneralViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='object-detail'),
    url(r'^api/simpleuser/', include(simpleuser_router.urls)),
    url(r'^api/accelerator/', include(schema_router.urls),
        name='api-root'),
    url(r'^sso/', include(sso_urlpatterns, namespace="sso")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(account_urlpatterns)),
    url(r'^graphql/$',
        csrf_exempt(SafeGraphQLView.as_view(
            graphiql=settings.DEBUG,
            schema=schema,
            middleware=[
                IsAuthenticatedMiddleware])),
        name="graphql"),
    url(r'^graphql/auth/$',
        csrf_exempt(SafeGraphQLView.as_view(
            graphiql=settings.DEBUG,
            schema=auth_schema)),
        name="graphql-auth"),
    url(r'^oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^schema/$', schema_view, name='schema'),
    url(r'^directory/(?:.*)$', TemplateView.as_view(
        template_name='front-end.html'),
        name="directory"),
    url(r'^allocator/(?:.*)$', TemplateView.as_view(
        template_name='front-end.html'),
        name="allocator"),
    url(r'^people/$', TemplateView.as_view(
        template_name='front-end.html'),
        name="entreprenuer_profile"),
    url(r'^people/(.*)/$', TemplateView.as_view(
        template_name='front-end.html'),
        name="entreprenuer_profile"),
    url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    url(r'^$', IndexView.as_view()),
]

# use staticfiles with gunicorn (not recommneded!)
# TODO: switch to a real static file handler
urls += (
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
if settings.DEBUG:
    # add debug toolbar
    import debug_toolbar  # pragma: no cover

    urls += [  # pragma: no cover
                url(r"^__debug__/", include(debug_toolbar.urls)),
                # pragma: no cover
            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urls
