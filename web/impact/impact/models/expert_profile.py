# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


import decimal

from django.db import models
from simpleuser.models import User

from impact.models.mc_model import MCModel
from impact.models.expert_category import ExpertCategory
from impact.models.functional_expertise import FunctionalExpertise
from impact.models.industry import Industry
from impact.models.mentoring_specialties import MentoringSpecialties
from impact.models.program_family import ProgramFamily
from impact.models.utils import is_managed


PRIVACY_CHOICES = (("staff", "MC Staff Only"),
                   ("finalists and staff", "Finalists and MC Staff"),
                   ("public", "All Users"), )

BASE_INTEREST = "I would like to participate in MassChallenge %s"

BASE_TOPIC = ("Please describe the topic(s) you would be available "
              "to speak%s about%s")

REF_BY_TEXT = ("If someone referred you to MassChallenge, please provide "
               "their name (and organization if relevant). Otherwise, please "
               "indicate how you learned about the opportunity to participate "
               "at MassChallenge (helps us understand the effectiveness of "
               "our outreach programs).")

OTHER_EXPERTS_TEXT = ("We're always looking for more great experts to join "
                      "the MassChallenge community and program. We welcome "
                      "the names and contact info (email) of individuals you "
                      "think could be great additions to the program, as well "
                      "as how you think they might want to be involved "
                      "(Judge, Mentor, etc.) Also, please encourage these "
                      "individuals to fill out their own Expert Profile.")

INVITED_JUDGE_ALERT = (
    "<h4>{first_name}, we would like to invite you to be a judge at "
    "MassChallenge!</h4>"
    "<p>&nbsp;</p>"
    "<p>{round_name} judging occurs from {start_date} to {end_date}! "
    "Of all our potential judges, we would like you, {first_name}, "
    "to take part."
    "</p><p>&nbsp;</p>"
    '<p><a class="btn btn-primary" href="/expert/commitments/">Click '
    "here to tell us your availability"
    "</a></p> <p>&nbsp;</p>"
)


class ExpertProfile(MCModel):
    user = models.OneToOneField(User)
    user_type = 'expert'
    phone = models.CharField(max_length=20)
    linked_in_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=16)
    personal_website_url = models.CharField(max_length=255)
    image = models.CharField(max_length=100)
    drupal_id = models.IntegerField(blank=True, null=True)
    drupal_creation_date = models.DateTimeField(blank=True, null=True)
    drupal_last_login = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=1)
    users_last_activity = models.DateTimeField(blank=True, null=True)
    current_program = models.ForeignKey('Program', blank=True, null=True)
    current_page = models.CharField(max_length=200)
    landing_page = models.CharField(max_length=200)
    privacy_policy_accepted = models.IntegerField()
    newsletter_sender = models.IntegerField()

    salutation = models.CharField(
        max_length=255,
        blank=True)
    title = models.CharField(
        max_length=255,
        verbose_name="Professional Title")
    company = models.CharField(
        max_length=255,
        verbose_name="Company Name")
    expert_category = models.ForeignKey(
        ExpertCategory,
        verbose_name="I primarily consider myself a",
        related_name="experts")
    functional_expertise = models.ManyToManyField(
        FunctionalExpertise,
        verbose_name="Functional Expertise",
        related_name="experts",
        blank=True)
    primary_industry = models.ForeignKey(
        Industry,
        verbose_name="Primary Industry",
        related_name="experts",
        limit_choices_to={'level__exact': 0})
    additional_industries = models.ManyToManyField(
        Industry,
        verbose_name="Additional Industries",
        related_name="secondary_experts",
        db_table="mc_expert_related_industry")
    privacy_email = models.CharField(
        max_length=64,
        verbose_name="Privacy - Email",
        choices=PRIVACY_CHOICES,
        default=PRIVACY_CHOICES[1][0])
    privacy_phone = models.CharField(
        max_length=64,
        verbose_name="Privacy - Phone",
        choices=PRIVACY_CHOICES,
        default=PRIVACY_CHOICES[1][0])
    privacy_web = models.CharField(
        max_length=64,
        verbose_name="Privacy - Web",
        choices=PRIVACY_CHOICES,
        default=PRIVACY_CHOICES[1][0])
    public_website_consent = models.BooleanField(
        verbose_name="Public Website Consent",
        blank=False,
        null=False,
        default=False)
    public_website_consent_checked = models.BooleanField(
        verbose_name="Public Website Consent Check",
        blank=False,
        null=False,
        default=False)
    judge_interest = models.BooleanField(
        verbose_name="Judge",
        help_text=BASE_INTEREST % 'as a Judge',
        default=False)
    mentor_interest = models.BooleanField(
        verbose_name="Mentor",
        help_text=BASE_INTEREST % 'as a Mentor',
        default=False)
    speaker_interest = models.BooleanField(
        verbose_name="Speaker",
        help_text=BASE_INTEREST % 'as a Speaker',
        default=False)
    speaker_topics = models.TextField(
        verbose_name="Speaker Topics",
        help_text=BASE_TOPIC % ('', ''),
        blank=True)
    office_hours_interest = models.BooleanField(
        verbose_name="Office Hours",
        help_text=BASE_INTEREST % 'by holding Office Hours',
        default=False)
    office_hours_topics = models.TextField(
        verbose_name="Office Hour Topics",
        help_text=BASE_TOPIC % (' to Finalists', ' during Office Hours'),
        blank=True)
    mentoring_specialties = models.ManyToManyField(
        MentoringSpecialties,
        verbose_name="Mentoring Specialties",
        db_table="mc_expert_related_mentoringspecialty",
        related_name="experts",
        blank=True)
    expert_group = models.CharField(
        verbose_name="Expert Group",
        max_length=10,
        blank=True)
    reliability = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=decimal.Decimal("1.00"),
        blank=True,
        null=True)
    referred_by = models.TextField(
        max_length=500,
        blank=True,
        help_text=REF_BY_TEXT)
    other_potential_experts = models.TextField(
        max_length=500,
        blank=True,
        help_text=OTHER_EXPERTS_TEXT)
    internal_notes = models.TextField(
        max_length=500,
        blank=True,
        help_text="Internal notes only for use by MassChallenge Staff "
                  "(not visible to Expert)")

    bio = models.TextField(blank=True, default="")
    home_program_family = models.ForeignKey(
        ProgramFamily,
        verbose_name="Home Program Family",
        blank=False,
        null=False)

    class Meta(MCModel.Meta):
        db_table = 'mc_expertprofile'
        managed = is_managed(db_table)
        permissions = (
            ('change_password', 'Can change users passwords directly'),
        )
