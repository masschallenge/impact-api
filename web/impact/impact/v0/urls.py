from django.conf.urls import url

from .v0.views import (
    MentorsProxyView,
    StartupListView,
    StartupDetailView,
)

v0_urlpatterns = [
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
