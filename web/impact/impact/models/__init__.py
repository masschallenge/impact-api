# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

# from paypal.pro.helpers import PayPalWPP  # Commented out for impact-api

from .startup_role import StartupRole
from .user_role import UserRole
from .program_cycle import ProgramCycle
from .base_profile import (
    BaseProfile,
    USER_TYPES,
)
from .program import (
    ACTIVE_PROGRAM_STATUS,
    CURRENT_STATUSES,
    ENDED_PROGRAM_STATUS,
    HIDDEN_PROGRAM_STATUS,
    Program,
    UPCOMING_PROGRAM_STATUS,
)
from .program_startup_status import (
    ProgramStartupStatus,
    STARTUP_BADGE_DISPLAY_VALUES,
)

from .startup_program_interest import (
    INTEREST_CHOICES,
    StartupProgramInterest,
)
from .startup_cycle_interest import StartupCycleInterest

from .recommendation_tag import RecommendationTag

from .program_administrator import ProgramAdministrator
from .site_program_authorization import SiteProgramAuthorization
from .mentor_program_office_hour import (
    LOCATION_CHOICES,
    MC_BOS_LOCATION,
    MC_CH_LOCATION,
    MC_IL_LOCATION,
    MC_MX_LOCATION,
    MC_NIC_LOCATION,
    MC_PULSE_LOCATION,
    MC_REMOTE_LOCATION,
    MC_UK_LOCATION,
    MentorProgramOfficeHour,
)
from .program_override import ProgramOverride
from .refund_code import RefundCode
from .observer import Observer
from .program_family import ProgramFamily
from .entrepreneur_profile import EntrepreneurProfile
from .expert_profile import ExpertProfile
from .functional_expertise import FunctionalExpertise
from .industry import Industry
from .member_profile import MemberProfile
from .named_group import NamedGroup
from .organization import Organization
from .partner import Partner
from .partner_team_member import PartnerTeamMember
from .program_manager import ProgramManager
from .program_role import ProgramRole
from .program_role_grant import ProgramRoleGrant
from .expert_interest import ExpertInterest
from .startup import (
    Startup,
    STARTUP_COMMUNITIES,
    DEFAULT_PROFILE_BACKGROUND_COLOR,
    DEFAULT_PROFILE_TEXT_COLOR,
)
from .application_type import ApplicationType
from .question import (
    CHOICE_LAYOUT_HORIZONTAL,
    CHOICE_LAYOUT_VERTICAL,
    CHOICE_LAYOUT_DROPDOWN,
    CHOICE_LAYOUTS,
    Question,
    QUESTION_TYPE_MULTILINE,
    QUESTION_TYPE_MULTICHOICE,
    QUESTION_TYPE_NUMBER,
    QUESTION_TYPES,
)
from .application_question import (
    ApplicationQuestion,
    TEXT_LIMIT_UNITS,
)
from .application_answer import ApplicationAnswer
from .application import (
    APPLICATION_STATUSES,
    Application,
    COMPLETE_APP_STATUS,
    DELAYED_STATUS,
    ERROR_PAYMENT_STATUS,
    FAILED_STATUS,
    INCOMPLETE_APP_STATUS,
    INSTANT_STATUS,
    NOT_ELIGIBLE_STATUS,
    PAID_PAYMENT_STATUS,
    PAYMENT_STATUSES,
    REFUND_STATUSES,
    REQUIRED_STATUS,
    SUBMITTED_APP_STATUS,
    UNPAID_PAYMENT_STATUS,
)

from impact.models.clearance import (
    Clearance,
    CLEARANCE_LEVEL_EXEC_MD,
    CLEARANCE_LEVEL_GLOBAL_MANAGER,
    CLEARANCE_LEVEL_ORDER,
    CLEARANCE_LEVEL_POM,
    CLEARANCE_LEVELS,
)

from .refund_code_redemption import RefundCodeRedemption
from .reference import Reference
from .startup_team_member import StartupTeamMember

from .program_startup_attribute import (
    ProgramStartupAttribute,
    ProgramStartupAttributeManager,
)
from .startup_attribute import StartupAttribute
from .startup_override_grant import StartupOverrideGrant
from .startup_status import StartupStatus
from .startup_mentor_tracking_record import (
    StartupMentorTrackingRecord,
)
from .startup_mentor_relationship import (
    CONFIRMED_RELATIONSHIP,
    DESIRED_RELATIONSHIP,
    DISCUSSING_RELATIONSHIP,
    RELATIONSHIP_CHOICES,
    StartupMentorRelationship,
)
from .interest_category import InterestCategory
from .expert_category import ExpertCategory
from .expert_interest_type import ExpertInterestType
from .job_posting import (
    JobPosting,
    JOB_TYPE_VALUES
)
from .newsletter_receipt import NewsletterReceipt
from .newsletter import Newsletter
from .section import (
    INCLUDE_FOR_CHOICES,
    Section,
)
from .program_partner import ProgramPartner
from .program_partner_type import (
    PARTNER_BADGE_DISPLAY_VALUES,
    ProgramPartnerType
)
from .site import Site
from .judging_form import JudgingForm

from .judge_application_feedback import (
    JUDGING_FEEDBACK_STATUS_COMPLETE,
    JUDGING_FEEDBACK_STATUS_CONFLICT,
    JUDGING_FEEDBACK_STATUS_ENUM,
    JUDGING_FEEDBACK_STATUS_INCOMPLETE,
    JUDGING_FEEDBACK_STATUS_OTHER,
    JUDGING_STATUS_CONFLICT,
    JUDGING_STATUS_ENUM,
    JUDGING_STATUS_NO_CONFLICT,
    JUDGING_STATUS_OTHER,
    JudgeApplicationFeedback,
)
from .judge_application_feedback_manager import (
    JudgeApplicationFeedbackManager
)
from .judge_availability import JudgeAvailability
from .judge_panel_assignment import (
    ASSIGNED_PANEL_ASSIGNMENT_STATUS,
    COMPLETE_PANEL_ASSIGNMENT_STATUS,
    JudgePanelAssignment,
)
from .judge_panel_assignment_manager import (
    JudgePanelAssignmentManager

)
from .judge_round_commitment import JudgeRoundCommitment
from .judging_form_element import JudgingFormElement
from .judging_round import (
    CAPTURE_AVAILABILITY_DISABLED,
    CAPTURE_AVAILABILITY_TIME,
    DEFAULT_BUFFER_BEFORE_EVENT,
    FEEDBACK_DISPLAY_DISABLED,
    IN_PERSON_JUDGING_ROUND_TYPE,
    JudgingRound,
    ONLINE_JUDGING_ROUND_TYPE,
    RECRUIT_NONE,
    RECRUIT_DISPLAY_ONLY,
    RECRUIT_ANYONE,
    RECRUIT_APPROVED_ONLY,

)

from .scenario import (
    DEFAULT_PANEL_SIZE,
    Scenario,
)
from .scenario_preference import (
    ALL_JUDGES,
    APPLICATION_ENTITY,
    ENTITY_TYPES,
    INDUSTRY_JUDGE_CATEGORIES,
    JUDGE_ALSO_KNOWS_INDUSTRY,
    JUDGE_CATEGORIES,
    JUDGE_ENTITY,
    JUDGE_GROUP_1,
    JUDGE_GROUP_2,
    JUDGE_GROUP_3,
    JUDGE_GROUP_4,
    JUDGE_GROUP_5,
    JUDGE_IN_INDUSTRY,
    JUDGE_IN_PROGRAM,
    JUDGE_IS_EXECUTIVE,
    JUDGE_IS_FEMALE,
    JUDGE_IS_INVESTOR,
    JUDGE_IS_LAWYER,
    JUDGE_IS_UNASSIGNED,
    JUDGE_KINDA_RELIABLE,
    JUDGE_MOST_RELIABLE,
    JUDGE_NOT_RELIABLE,
    JUDGE_OUTSIDE_PROGRAM,
    MAX_PREFERENCE,
    MIN_PREFERENCE,
    PREFERENCE_CONSTRAINT_TYPES,
    PROGRAM_JUDGE_CATEGORIES,
    SIMPLE_JUDGE_CATEGORIES,
    SPECIAL_JUDGE_CATEGORIES,
    ScenarioPreference,
)
from .scenario_application import ScenarioApplication
from .scenario_judge import ScenarioJudge
from .mentoring_specialties import MentoringSpecialties
from .panel import (
    ACTIVE_PANEL_STATUS,
    COMPLETED_PANEL_STATUS,
    DEFAULT_PANEL_STATUS,
    PANEL_STATUS_ENUM,
    PREVIEW_PANEL_STATUS,
    Panel,
)
from .judge_feedback_component import (
    JUDGE_FEEDBACK_REVIEWER,
    JUDGE_FEEDBACK_SANITIZER,
    JudgeFeedbackComponent,
)

from .panel_location import PanelLocation
from .panel_time import PanelTime
from .panel_type import PanelType
from .application_panel_assignment import ApplicationPanelAssignment

from .paypal_payment import PayPalPayment
from .paypal_refund import PayPalRefund
from .startup_label import StartupLabel
from .user_label import UserLabel
from .program_administrator_permission import (
    ProgramAdministratorPermission
)
from .bucket_state import (
    BucketState,
    BUCKET_TYPES,
    NEW_ENTREPRENEURS_BUCKET_TYPE,
    STALE_NOSTARTUP_BUCKET_TYPE,
    STALE_STARTUP_BUCKET_TYPE,
    SUBMITTED_BUCKET_TYPE,
    UNPAID_BUCKET_TYPE,
    UNSUBMITTED_BUCKET_TYPE,
)
