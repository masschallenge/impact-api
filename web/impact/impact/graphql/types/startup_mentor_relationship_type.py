import graphene
from graphene_django import DjangoObjectType

from accelerator.models import StartupMentorRelationship
from impact.graphql.types.expert_startup_type import ExpertStartupType


class StartupMentorRelationshipType(DjangoObjectType):
    startup = graphene.Field(ExpertStartupType)
    program_status = graphene.String()

    class Meta:
        model = StartupMentorRelationship

    def resolve_program_status(self, info, **kwargs):
        program = self.startup_mentor_tracking.program
        return program and program.program_status

    def resolve_startup(self, info, **kwargs):
        info.variable_values["startup_mentor_relationship_id"] = self.id
        return self.startup_mentor_tracking.startup
