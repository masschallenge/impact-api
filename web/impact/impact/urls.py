# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from impact.schema import schema_view
from impact.views import (
    GeneralViewSet,
    IndexView,
)
from impact.v0.views import (
    ImageProxyView,
    JobPostingDetailView,
    JobPostingListView,
    MentorsProxyView,
    StartupListView,
    StartupDetailView,
)
from impact.v1.views import (
    IndustryDetailView,
    IndustryListView,
    OrganizationDetailView,
    OrganizationHistoryView,
    OrganizationListView,
    OrganizationUsersView,
    UserDetailView,
    UserHistoryView,
    UserListView,
    UserOrganizationsView,
)
from rest_framework import routers
from drf_auto_endpoint.router import router as schema_router
from django.apps import apps


accelerator_router = routers.DefaultRouter()
simpleuser_router = routers.DefaultRouter()

simpleuser_router.register('User', GeneralViewSet, base_name='User')

for model in apps.get_models('impact'):
    if model._meta.app_label == 'impact':
        schema_router.register(model, url=model.__name__)


for model in apps.get_models('accelerator'):
    if model._meta.app_label == 'accelerator' and hasattr(model, "Meta"):
        accelerator_router.register(
            model.__name__, GeneralViewSet,
            base_name="accelerator.{model}".format(model=model.__name__))

account_urlpatterns = [
    url(r'^', include('registration.backends.simple.urls')),
]

v0_urlpatterns = [
    url(r"^image/$",
        ImageProxyView.as_view(),
        name="image"),
    url(r"^job_posting_list/$",
        JobPostingListView.as_view(),
        name="job_posting_list"),
    url(r"^job_posting_detail/$",
        JobPostingDetailView.as_view(),
        name="job_posting_detail"),
    url(r"^mentors/$",
        MentorsProxyView.as_view(),
        name="mentors"),
    url(r"^startup_list/$",
        StartupListView.as_view(),
        name="startup_list"),
    url(r"^startup_detail/$",
        StartupDetailView.as_view(),
        name="startup_detail"),
]

v1_urlpatterns = [
    url(r"^industry/(?P<pk>[0-9]+)/$",
        IndustryDetailView.as_view(),
        name="industry_detail"),
    url(r"^industry/$",
        IndustryListView.as_view(),
        name="industry"),

    url(r"^organization/(?P<pk>[0-9]+)/$",
        OrganizationDetailView.as_view(),
        name="organization_detail"),
    url(r"^organization/(?P<pk>[0-9]+)/history/$",
        OrganizationHistoryView.as_view(),
        name="organization_history"),
    url(r"^organization/$",
        OrganizationListView.as_view(),
        name="organization"),
    url(r"^organization/(?P<pk>[0-9]+)/users/$",
        OrganizationUsersView.as_view(),
        name="organization_users"),

    url(r"^user/(?P<pk>[0-9]+)/$",
        UserDetailView.as_view(),
        name="user_detail"),
    url(r"^user/(?P<pk>[0-9]+)/history/$",
        UserHistoryView.as_view(),
        name="user_history"),
    url(r"^user/$",
        UserListView.as_view(),
        name="user"),
    url(r"^user/(?P<pk>[0-9]+)/organizations/$",
        UserOrganizationsView.as_view(),
        name="user_organizations"),
]

urls = [
    url(r"^api/v0/", include(v0_urlpatterns)),
    url(r"^api/v1/", include(v1_urlpatterns)),
    url(r'^api/(?P<app>\w+)/(?P<model>\w+)/$',
        GeneralViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='object-list'),
    url(r'^api/(?P<app>\w+)/(?P<model>\w+)/(?P<pk>[0-9]+)/$',
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
    url(r'^$', IndexView.as_view()),
    url(r'^accounts/', include(account_urlpatterns)),
    url(r'^schema/$', schema_view, name='schema'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include(
        'oauth2_provider.urls',
        namespace='oauth2_provider'))
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
