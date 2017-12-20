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
    ProgramCycleDetailView,
    ProgramCycleListView,
    ProgramDetailView,
    ProgramFamilyDetailView,
    ProgramFamilyListView,
    ProgramListView,
    UserConfidentialView,
    UserDetailView,
    UserHistoryView,
    UserListView,
    UserOrganizationsView,
)

accelerator_router = routers.DefaultRouter()
simpleuser_router = routers.DefaultRouter()

simpleuser_router.register('User', GeneralViewSet, base_name='User')

for model in apps.get_models('impact'):
    if model._meta.app_label == 'impact' and not model._meta.auto_created:
        schema_router.register(model, url=model_name_to_snake(model.__name__))

for model in apps.get_models('accelerator'):
    if (
            model._meta.app_label == 'accelerator'
            and hasattr(model, "Meta")
            and not model._meta.auto_created
    ):
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
        name=IndustryDetailView.view_name),
    url(r"^industry/$",
        IndustryListView.as_view(),
        name=IndustryListView.view_name),

    url(r"^organization/(?P<pk>[0-9]+)/$",
        OrganizationDetailView.as_view(),
        name=OrganizationDetailView.view_name),
    url(r"^organization/(?P<pk>[0-9]+)/history/$",
        OrganizationHistoryView.as_view(),
        name=OrganizationHistoryView.view_name),
    url(r"^organization/$",
        OrganizationListView.as_view(),
        name=OrganizationListView.view_name),
    url(r"^organization/(?P<pk>[0-9]+)/users/$",
        OrganizationUsersView.as_view(),
        name=OrganizationUsersView.view_name),

    url(r"^program/(?P<pk>[0-9]+)/$",
        ProgramDetailView.as_view(),
        name=ProgramDetailView.view_name),
    url(r"^program/$",
        ProgramListView.as_view(),
        name=ProgramListView.view_name),

    url(r"^program_cycle/(?P<pk>[0-9]+)/$",
        ProgramCycleDetailView.as_view(),
        name=ProgramCycleDetailView.view_name),
    url(r"^program_cycle/$",
        ProgramCycleListView.as_view(),
        name=ProgramCycleListView.view_name),

    url(r"^program_family/(?P<pk>[0-9]+)/$",
        ProgramFamilyDetailView.as_view(),
        name=ProgramFamilyDetailView.view_name),
    url(r"^program_family/$",
        ProgramFamilyListView.as_view(),
        name=ProgramFamilyListView.view_name),

    url(r"^user/(?P<pk>[0-9]+)/confidential/$",
        UserConfidentialView.as_view(),
        name=UserConfidentialView.view_name),
    url(r"^user/(?P<pk>[0-9]+)/$",
        UserDetailView.as_view(),
        name=UserDetailView.view_name),
    url(r"^user/(?P<pk>[0-9]+)/history/$",
        UserHistoryView.as_view(),
        name=UserHistoryView.view_name),
    url(r"^user/$",
        UserListView.as_view(),
        name=UserListView.view_name),
    url(r"^user/(?P<pk>[0-9]+)/organizations/$",
        UserOrganizationsView.as_view(),
        name=UserOrganizationsView.view_name),
]

jwt_urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

urls = [
    url(r"^api/v0/", include(v0_urlpatterns)),
    url(r"^api/v1/", include(v1_urlpatterns)),
    url(r"^api/jwt/", include(jwt_urlpatterns)),
    url(
        r'^api/(?P<app>\w+)/(?P<model>[a-z_]+)/'
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
