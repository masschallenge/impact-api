import graphene
from graphene_django import DjangoObjectType

from mc.models import StartupMentorRelationship
from .program_type import ProgramType
from .expert_startup_type import ExpertStartupType


class StartupMentorRelationshipType(DjangoObjectType):
    startup = graphene.Field(ExpertStartupType)
    program = graphene.Field(ProgramType)

    class Meta:
        model = StartupMentorRelationship

    def resolve_program(self, info, **kwargs):
        return self.startup_mentor_tracking.program

    def resolve_startup(self, info, **kwargs):
        info.variable_values["startup_mentor_relationship_id"] = self.id
        return self.startup_mentor_tracking.startup
