# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from simpleuser.models import User
from impact.models.mc_model import MCModel
from impact.models.utils import is_managed


class MemberProfile(MCModel):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    linked_in_url = models.CharField(max_length=200)
    facebook_url = models.CharField(max_length=200)
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

    class Meta(MCModel.Meta):
        db_table = 'mc_memberprofile'
        managed = is_managed(db_table)
