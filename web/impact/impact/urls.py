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
    UserDetailView,
    UserListView,
    OrganizationDetailView,
    OrganizationListView,
)
from rest_framework import routers

impact_router = routers.DefaultRouter()
simpleuser_router = routers.DefaultRouter()

simpleuser_router.register('User', GeneralViewSet, base_name='User')
impact_router.register('Organization', GeneralViewSet, base_name='Organization')
impact_router.register('Application', GeneralViewSet, base_name='Application')
impact_router.register('ApplicationAnswer', GeneralViewSet,
                       base_name='ApplicationAnswer')
impact_router.register('ApplicationPanelAssignment',
                       GeneralViewSet, base_name='ApplicationPanelAssignment')
impact_router.register('ApplicationQuestion',
                       GeneralViewSet, base_name='ApplicationQuestion')
impact_router.register('ApplicationType', GeneralViewSet,
                       base_name='ApplicationType')
impact_router.register('BaseProfile', GeneralViewSet, base_name='BaseProfile')
impact_router.register('Country', GeneralViewSet, base_name='Country')
impact_router.register('Currency', GeneralViewSet, base_name='Currency')
impact_router.register('EntrepreneurProfile',
                       GeneralViewSet, base_name='EntrepreneurProfile')
impact_router.register('EntrepreneurProfileInterestCategories',
                       GeneralViewSet,
                       base_name='EntrepreneurProfileInterestCategories')
impact_router.register('EntrepreneurProfileProgramFamilies',
                       GeneralViewSet,
                       base_name='EntrepreneurProfileProgramFamilies')
impact_router.register('EntrepreneurProfileRecommendationTags',
                       GeneralViewSet,
                       base_name='EntrepreneurProfileRecommendationTags')
impact_router.register('ExpertRelatedIndustry',
                       GeneralViewSet, base_name='ExpertRelatedIndustry')
impact_router.register('ExpertRelatedMentoringSpecialty',
                       GeneralViewSet,
                       base_name='ExpertRelatedMentoringSpecialty')
impact_router.register('ExpertCategory', GeneralViewSet,
                       base_name='ExpertCategory')
impact_router.register('ExpertInterest', GeneralViewSet,
                       base_name='ExpertInterest')
impact_router.register('ExpertInterestType', GeneralViewSet,
                       base_name='ExpertInterestType')
impact_router.register('ExpertProfile', GeneralViewSet,
                       base_name='ExpertProfile')
impact_router.register('ExpertProfileFunctionalExpertise',
                       GeneralViewSet,
                       base_name='ExpertProfileFunctionalExpertise')
impact_router.register('ExpertProfileInterestCategories',
                       GeneralViewSet,
                       base_name='ExpertProfileInterestCategories')
impact_router.register('ExpertProfileProgramFamilies',
                       GeneralViewSet,
                       base_name='ExpertProfileProgramFamilies')
impact_router.register('ExpertProfileRecommendationTags',
                       GeneralViewSet,
                       base_name='ExpertProfileRecommendationTags')
impact_router.register('FunctionalExpertise',
                       GeneralViewSet, base_name='FunctionalExpertise')
impact_router.register('Industry', GeneralViewSet, base_name='Industry')
impact_router.register('InterestCategory', GeneralViewSet,
                       base_name='InterestCategory')
impact_router.register('JobPosting', GeneralViewSet, base_name='JobPosting')
impact_router.register('JudgeApplicationFeedback',
                       GeneralViewSet, base_name='JudgeApplicationFeedback')
impact_router.register('JudgeAvailability', GeneralViewSet,
                       base_name='JudgeAvailability')
impact_router.register('JudgeFeedbackComponent',
                       GeneralViewSet, base_name='JudgeFeedbackComponent')
impact_router.register('JudgePanelAssignment',
                       GeneralViewSet, base_name='JudgePanelAssignment')
impact_router.register('JudgeQuotaRule', GeneralViewSet,
                       base_name='JudgeQuotaRule')
impact_router.register('JudgeRoundCommitment',
                       GeneralViewSet, base_name='JudgeRoundCommitment')
impact_router.register('JudgingForm', GeneralViewSet, base_name='JudgingForm')
impact_router.register('JudgingFormElement', GeneralViewSet,
                       base_name='JudgingFormElement')
impact_router.register('JudgingRound', GeneralViewSet,
                       base_name='JudgingRound')
impact_router.register('JudgingRoundStage', GeneralViewSet,
                       base_name='JudgingRoundStage')
impact_router.register('MemberProfile', GeneralViewSet,
                       base_name='MemberProfile')
impact_router.register('MemberProfileInterestCategories',
                       GeneralViewSet,
                       base_name='MemberProfileInterestCategories')
impact_router.register('MemberProfileProgramFamilies',
                       GeneralViewSet,
                       base_name='MemberProfileProgramFamilies')
impact_router.register('MemberProfileRecommendationTags',
                       GeneralViewSet,
                       base_name='MemberProfileRecommendationTags')
impact_router.register('MentoringSpecialties',
                       GeneralViewSet,
                       base_name='MentoringSpecialties')
impact_router.register('MentorProgramOfficeHour',
                       GeneralViewSet, base_name='MentorProgramOfficeHour')
impact_router.register('NamedGroup', GeneralViewSet, base_name='NamedGroup')
impact_router.register('Newsletter', GeneralViewSet, base_name='Newsletter')
impact_router.register('NewsletterRecipientRoles',
                       GeneralViewSet, base_name='NewsletterRecipientRoles')
impact_router.register('NewsletterReceipt', GeneralViewSet,
                       base_name='NewsletterReceipt')
impact_router.register('Observer', GeneralViewSet, base_name='Observer')
impact_router.register('ObserverNewsletterCcRoles',
                       GeneralViewSet, base_name='ObserverNewsletterCcRoles')
impact_router.register('Panel', GeneralViewSet, base_name='Panel')
impact_router.register('PanelSequenceUpdates',
                       GeneralViewSet, base_name='PanelSequenceUpdates')
impact_router.register('PanelLocation', GeneralViewSet,
                       base_name='PanelLocation')
impact_router.register('PanelTime', GeneralViewSet, base_name='PanelTime')
impact_router.register('PanelType', GeneralViewSet, base_name='PanelType')
impact_router.register('Partner', GeneralViewSet, base_name='Partner')
impact_router.register('PartnerTeamMember', GeneralViewSet,
                       base_name='PartnerTeamMember')
impact_router.register('PayPalPayment', GeneralViewSet,
                       base_name='PayPalPayment')
impact_router.register('PayPalRefund', GeneralViewSet,
                       base_name='PayPalRefund')
impact_router.register('Program', GeneralViewSet, base_name='Program')
impact_router.register('ProgramAdministrator',
                       GeneralViewSet, base_name='ProgramAdministrator')
impact_router.register('ProgramAdministratorPermission',
                       GeneralViewSet,
                       base_name='ProgramAdministratorPermission')
impact_router.register('ProgramCycle', GeneralViewSet,
                       base_name='ProgramCycle')
impact_router.register('ProgramFamily', GeneralViewSet,
                       base_name='ProgramFamily')
impact_router.register('ProgramOverride', GeneralViewSet,
                       base_name='ProgramOverride')
impact_router.register('ProgramPartner', GeneralViewSet,
                       base_name='ProgramPartner')
impact_router.register('ProgramPartnerType', GeneralViewSet,
                       base_name='ProgramPartnerType')
impact_router.register('ProgramRole', GeneralViewSet, base_name='ProgramRole')
impact_router.register('ProgramRoleGrant', GeneralViewSet,
                       base_name='ProgramRoleGrant')
impact_router.register('ProgramStartupAttribute',
                       GeneralViewSet, base_name='ProgramStartupAttribute')
impact_router.register('ProgramStartupStatus',
                       GeneralViewSet, base_name='ProgramStartupStatus')
impact_router.register('Question', GeneralViewSet, base_name='Question')
impact_router.register('RecommendationTag', GeneralViewSet,
                       base_name='RecommendationTag')
impact_router.register('Reference', GeneralViewSet, base_name='Reference')
impact_router.register('RefundCode', GeneralViewSet, base_name='RefundCode')
impact_router.register('RefundCodePrograms', GeneralViewSet,
                       base_name='RefundCodePrograms')
impact_router.register('RefundCodeRedemption',
                       GeneralViewSet, base_name='RefundCodeRedemption')
impact_router.register('Scenario', GeneralViewSet, base_name='Scenario')
impact_router.register('ScenarioApplication',
                       GeneralViewSet, base_name='ScenarioApplication')
impact_router.register('ScenarioJudge', GeneralViewSet,
                       base_name='ScenarioJudge')
impact_router.register('ScenarioPreference', GeneralViewSet,
                       base_name='ScenarioPreference')
impact_router.register('Section', GeneralViewSet, base_name='Section')
impact_router.register('SectionInterestCategories',
                       GeneralViewSet, base_name='SectionInterestCategories')
impact_router.register('Site', GeneralViewSet, base_name='Site')
impact_router.register('SiteProgramAuthorization',
                       GeneralViewSet, base_name='SiteProgramAuthorization')
impact_router.register('Startup', GeneralViewSet, base_name='Startup')
impact_router.register('StartupRecommendationTags',
                       GeneralViewSet, base_name='StartupRecommendationTags')
impact_router.register('StartupRelatedIndustry',
                       GeneralViewSet, base_name='StartupRelatedIndustry')
impact_router.register('StartupAttribute', GeneralViewSet,
                       base_name='StartupAttribute')
impact_router.register('StartupCycleInterest',
                       GeneralViewSet, base_name='StartupCycleInterest')
impact_router.register('StartupLabel', GeneralViewSet,
                       base_name='StartupLabel')
impact_router.register('StartupLabelStartups',
                       GeneralViewSet, base_name='StartupLabelStartups')
impact_router.register('StartupMentorRelationship',
                       GeneralViewSet, base_name='StartupMentorRelationship')
impact_router.register('StartupMentorTrackingRecord',
                       GeneralViewSet, base_name='StartupMentorTrackingRecord')
impact_router.register('StartupOverrideGrant',
                       GeneralViewSet, base_name='StartupOverrideGrant')
impact_router.register('StartupProgramInterest',
                       GeneralViewSet, base_name='StartupProgramInterest')
impact_router.register('StartupRole', GeneralViewSet, base_name='StartupRole')
impact_router.register('StartupStatus', GeneralViewSet,
                       base_name='StartupStatus')
impact_router.register('StartupTeamMember', GeneralViewSet,
                       base_name='StartupTeamMember')
impact_router.register('StartupTeamMemberRecommendationTags',
                       GeneralViewSet,
                       base_name='StartupTeamMemberRecommendationTags')
impact_router.register('UsState', GeneralViewSet, base_name='UsState')
impact_router.register('UserLabel', GeneralViewSet, base_name='UserLabel')
impact_router.register('UserLabelUsers', GeneralViewSet,
                       base_name='UserLabelUsers')
impact_router.register('UserProfile', GeneralViewSet, base_name='UserProfile')
impact_router.register('UserRole', GeneralViewSet, base_name='UserRole')

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
    url(r"^user/(?P<pk>[0-9]+)/$",
        UserDetailView.as_view(),
        name="user_detail"),
    url(r"^user/$",
        UserListView.as_view(),
        name="user"),
    url(r"^organization_detail/(?P<pk>[0-9]+)/$",
        OrganizationDetailView.as_view(),
        name="organization_detail"),
    url(r"^organization/$",
        OrganizationListView.as_view(),
        name="organization"),
    
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
    url(r'^api/impact/', include(impact_router.urls), name='api-root'),
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
