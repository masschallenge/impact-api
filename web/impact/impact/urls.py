# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from drf_auto_endpoint.router import router as schema_router
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from impact.models.utils import model_name_to_snake
from impact.schema import schema_view
from impact.utils import model_is_not_auto_created
from impact.v0.urls import v0_urlpatterns
from impact.v1.urls import v1_urlpatterns
from impact.views import (
    GeneralViewSet,
    IndexView,
)

accelerator_router = routers.DefaultRouter()
simpleuser_router = routers.DefaultRouter()
simpleuser_router.register('User', GeneralViewSet, base_name='User')

for model in apps.get_models('impact'):
    if model._meta.app_label == 'impact' and not model._meta.auto_created:
        schema_router.register(model, url=model_name_to_snake(model.__name__))

for model in apps.get_models('accelerator'):
    if model_is_not_auto_created(model, app_label='accelerator'):
        accelerator_router.register(
            model.__name__, GeneralViewSet,
            base_name="accelerator.{model}".format(model=model.__name__))

sso_urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]

account_urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
]

urls = [
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
    url(r'^api/accelerator/', include(accelerator_router.urls)),
    url(r'^api/impact/', include(schema_router.urls), name='api-root'),
    url(r'^sso/', include(sso_urlpatterns, namespace="sso")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(account_urlpatterns)),
    url(r'^oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^schema/$', schema_view, name='schema'),
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
        url(r"^__debug__/", include(debug_toolbar.urls)),  # pragma: no cover
    ]

urlpatterns = urls
