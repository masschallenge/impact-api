# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
try:
    from sorl.thumbnail import ImageField
    HAS_SORL = True
except ImportError:
    HAS_SORL = False

from impact.models.mc_model import MCModel
from impact.models.program import Program
from impact.models.startup import Startup
from impact.models.startup_role import StartupRole
from impact.models.utils import is_managed

STARTUP_BADGE_DISPLAY_VALUES = (
    ('NONE', 'None'),
    ('STARTUP_LIST', 'Only on startup list'),
    ('STARTUP_PROFILE', 'Only on startup profile'),
    ('STARTUP_LIST_AND_PROFILE', 'Startup list and profile'))


class ProgramStartupStatus(MCModel):
    program = models.ForeignKey(Program)
    startup_status = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    startup_role = models.ForeignKey(StartupRole,
                                     null=True,
                                     blank=True)
    startup_list_include = models.BooleanField(
        default=False,
        help_text=("Include this startup status as a tab "
                   "in the public startup list"))
    startup_list_tab_title = models.CharField(max_length=50, null=True)
    startup_list_tab_description = models.TextField(
        max_length=1000,
        blank=True,
        help_text="You may use HTML, including links")
    startup_list_tab_id = models.CharField(
        max_length=30,
        null=True,
        help_text="The slug used in the public URL")
    startup_list_tab_order = models.IntegerField(null=True)
    include_stealth_startup_names = models.BooleanField(default=False)
    if HAS_SORL:
        badge_image = ImageField(
            upload_to='badge_images',
            blank=True)
    else:
        badge_image = models.CharField(max_length=100, null=True)

    badge_display = models.CharField(choices=STARTUP_BADGE_DISPLAY_VALUES,
                                     max_length=30, default="NONE")
    status_group = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Only one status is shown from the same status group; "
        "which one is determined by sort order")
    sort_order = models.IntegerField(
        blank=True,
        null=True,
        help_text="Order")

    class Meta(MCModel.Meta):
        db_table = 'accelerator_programstartupstatus'
        managed = is_managed(db_table)
        verbose_name_plural = 'Program Startup Statuses'
        ordering = ['program', 'sort_order', 'startup_status']

    def __str__(self):
        return "%s (Program Startup Status for %s)" % (self.startup_status,
                                                       self.program)

    def startups(self):
        return Startup.objects.filter(
            startupstatus__program_startup_status=self)
