from django.conf.urls import url

from impact.v1.views import (
    ApplicationDetailView,
    AllocateApplicationsView,
    AnalyzeJudgingRoundView,
    ApplicationListView,
    CloneCriteriaView,
    CreditCodeDetailView,
    CreditCodeListView,
    CriterionDetailView,
    CriterionListView,
    CriterionOptionSpecDetailView,
    CriterionOptionSpecListView,
    FunctionalExpertiseDetailView,
    FunctionalExpertiseListView,
    IndustryDetailView,
    IndustryListView,
    JudgingRoundCriteriaHeaderView,
    JudgingRoundDetailView,
    JudgingRoundListView,
    OrganizationDetailView,
    OrganizationHistoryView,
    OrganizationListView,
    OrganizationUsersView,
    ProgramDetailView,
    ProgramListView,
    ProgramCycleDetailView,
    ProgramCycleListView,
    ProgramFamilyDetailView,
    ProgramFamilyListView,
    UserConfidentialView,
    UserDetailView,
    UserHistoryView,
    UserListView,
    UserOrganizationsView
)

v1_urlpatterns = [
    url(r"^allocate_applications/(?P<round_id>[0-9]+)/(?P<judge_id>[0-9]+)/$",
        AllocateApplicationsView.as_view(),
        name=AllocateApplicationsView.view_name),
    url(r"^analyze_judging_round/(?P<pk>[0-9]+)/$",
        AnalyzeJudgingRoundView.as_view(),
        name=AnalyzeJudgingRoundView.view_name),
    url(r"^application/(?P<pk>[0-9]+)/$",
        ApplicationDetailView.as_view(),
        name=ApplicationDetailView.view_name),
    url(r"^application/$",
        ApplicationListView.as_view(),
        name=ApplicationListView.view_name),
    url(r"^clone_criteria/$",
        CloneCriteriaView.as_view(),
        name=CloneCriteriaView.view_name),
    url(r"^credit_code/(?P<pk>[0-9]+)/$",
        CreditCodeDetailView.as_view(),
        name=CreditCodeDetailView.view_name),
    url(r"^credit_code/$",
        CreditCodeListView.as_view(),
        name=CreditCodeListView.view_name),
    url(r"^functional_expertise/(?P<pk>[0-9]+)/$",
        FunctionalExpertiseDetailView.as_view(),
        name=FunctionalExpertiseDetailView.view_name),
    url(r"^functional_expertise/$",
        FunctionalExpertiseListView.as_view(),
        name=FunctionalExpertiseListView.view_name),
    url(r"^industry/(?P<pk>[0-9]+)/$",
        IndustryDetailView.as_view(),
        name=IndustryDetailView.view_name),
    url(r"^industry/$",
        IndustryListView.as_view(),
        name=IndustryListView.view_name),
    url(r"^judging_round/(?P<pk>[0-9]+)/$",
        JudgingRoundDetailView.as_view(),
        name=JudgingRoundDetailView.view_name),
    url(r"^judging_round/$",
        JudgingRoundListView.as_view(),
        name=JudgingRoundListView.view_name),
    url(r"^judging_round_criteria_header/(?P<pk>[0-9]+)/$",
        JudgingRoundCriteriaHeaderView.as_view(),
        name=JudgingRoundCriteriaHeaderView.view_name),
    url(r"^criterion/(?P<pk>[0-9]+)/$",
        CriterionDetailView.as_view(),
        name=CriterionDetailView.view_name),
    url(r"^criterion/$",
        CriterionListView.as_view(),
        name=CriterionListView.view_name),
    url(r"^criterion_option_spec/(?P<pk>[0-9]+)/$",
        CriterionOptionSpecDetailView.as_view(),
        name=CriterionOptionSpecDetailView.view_name),
    url(r"^criterion_option_spec/$",
        CriterionOptionSpecListView.as_view(),
        name=CriterionOptionSpecListView.view_name),
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
