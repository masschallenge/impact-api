# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models

from impact.models.mc_model import MCModel
from impact.models.scenario import Scenario
from impact.models.utils import is_managed


ALL_JUDGES = "all"
JUDGE_GROUP_1 = "group_1"
JUDGE_GROUP_2 = "group_2"
JUDGE_GROUP_3 = "group_3"
JUDGE_GROUP_4 = "group_4"
JUDGE_GROUP_5 = "group_5"
JUDGE_IS_EXECUTIVE = "is_executive"
JUDGE_IS_FEMALE = "is_female"
JUDGE_IS_INVESTOR = "is_investor"
JUDGE_IS_LAWYER = "is_lawyer"
JUDGE_KINDA_RELIABLE = "kinda_reliable"
JUDGE_MOST_RELIABLE = "most_reliable"
JUDGE_NOT_RELIABLE = "not_reliable"
SIMPLE_JUDGE_CATEGORIES = [
    (ALL_JUDGES, 'Judges Overall'),
    (JUDGE_IS_FEMALE, 'Judges that are Female'),
    (JUDGE_IS_LAWYER, 'Judges that are Lawyers'),
    (JUDGE_IS_EXECUTIVE, 'Judges that are Executives'),
    (JUDGE_IS_INVESTOR, 'Judges that are Investors'),
    (JUDGE_GROUP_1, 'Judges in Group 1'),
    (JUDGE_GROUP_2, 'Judges in Group 2'),
    (JUDGE_GROUP_3, 'Judges in Group 3'),
    (JUDGE_GROUP_4, 'Judges in Group 4'),
    (JUDGE_GROUP_5, 'Judges in Group 5'),
    (JUDGE_MOST_RELIABLE, 'Judges that are the most reliable'),
    (JUDGE_KINDA_RELIABLE, 'Judges that are kinda reliable'),
    (JUDGE_NOT_RELIABLE, 'Judges that are not reliable'),
]


JUDGE_IS_UNASSIGNED = "is_unassigned"
SPECIAL_JUDGE_CATEGORIES = [
    (JUDGE_IS_UNASSIGNED, 'Judges that were not assigned this round'),
]


JUDGE_ALSO_KNOWS_INDUSTRY = "also_knows_industry"
JUDGE_IN_INDUSTRY = "expert_in_industry"
INDUSTRY_JUDGE_CATEGORIES = [
    (JUDGE_IN_INDUSTRY,
     'Judges w/ expertise in the startup\'s primary industry'),
    (JUDGE_ALSO_KNOWS_INDUSTRY,
     'Judges w/ secondary expertise in the startup\'s primary industry'),
]


JUDGE_IN_PROGRAM = "in_program"
JUDGE_OUTSIDE_PROGRAM = "outside_program"
PROGRAM_JUDGE_CATEGORIES = [
    ('in_program',
     'Judges in program startup is applying to'),
    ('outside_program',
     'Judges not in program startup is applying to'),
]


JUDGE_CATEGORIES = (SIMPLE_JUDGE_CATEGORIES +
                    SPECIAL_JUDGE_CATEGORIES +
                    INDUSTRY_JUDGE_CATEGORIES +
                    PROGRAM_JUDGE_CATEGORIES)


MAX_PREFERENCE = "max"
MIN_PREFERENCE = "min"
PREFERENCE_CONSTRAINT_TYPES = (
    (MAX_PREFERENCE, 'Maximum number of'),
    (MIN_PREFERENCE, 'Minimum number of'),
)


JUDGE_ENTITY = "JUDGE"
APPLICATION_ENTITY = "APPLICATION"
ENTITY_TYPES = (
    (JUDGE_ENTITY, 'judge'),
    (APPLICATION_ENTITY, 'application'))


class ScenarioPreference(MCModel):
    scenario = models.ForeignKey(Scenario)
    priority = models.PositiveIntegerField(null=False)
    constraint_type = models.CharField(max_length=16,
                                       null=False,
                                       blank=False,
                                       choices=PREFERENCE_CONSTRAINT_TYPES)
    entity_type = models.CharField(max_length=16,
                                   null=False,
                                   blank=False,
                                   choices=(ENTITY_TYPES))
    entity_set = models.CharField(max_length=32,
                                  null=False,
                                  blank=False,
                                  choices=JUDGE_CATEGORIES)
    amount = models.PositiveIntegerField(default=1,
                                         null=True,
                                         blank=True)

    class Meta(MCModel.Meta):
        db_table = 'mc_scenariopreference'
        managed = is_managed(db_table)
        unique_together = ('scenario', 'priority', 'entity_type')
        ordering = ['priority']

    def __str__(self):
        return "{0}_{1}s_{2}{3}".format(
            self.constraint_type.lower(),
            self.entity_type.lower(),
            self.entity_set.lower(),
            '_is_' + str(self.amount) if self.amount else '')
