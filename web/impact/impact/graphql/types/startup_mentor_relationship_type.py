import graphene
from graphene_django import DjangoObjectType

from accelerator.models import StartupMentorRelationship


class StartupMentorRelationshipType(DjangoObjectType):
    program_location = graphene.String()
    program_status = graphene.String()
    program_year = graphene.String()
    startup_id = graphene.String()
    startup_name = graphene.String()
    startup_high_resolution_logo = graphene.String()
    startup_short_pitch = graphene.String()

    class Meta:
        model = StartupMentorRelationship

    def resolve_program_location(self, info, **kwargs):
        program = self.startup_mentor_tracking.program
        return program and program.program_family.name

    def resolve_program_year(self, info, **kwargs):
        program = self.startup_mentor_tracking.program
        return program and program.start_date.year

    def resolve_program_status(self, info, **kwargs):
        program = self.startup_mentor_tracking.program
        return program and program.program_status

    def resolve_startup_id(self, info, **kwargs):
        startup = self.startup_mentor_tracking.startup
        return startup and startup.id

    def resolve_startup_name(self, info, **kwargs):
        startup = self.startup_mentor_tracking.startup
        return startup and startup.name

    def resolve_startup_high_resolution_logo(self, info, **kwargs):
        startup = self.startup_mentor_tracking.startup
        return startup and startup.high_resolution_logo

    def resolve_startup_short_pitch(self, info, **kwargs):
        startup = self.startup_mentor_tracking.startup
        return startup and startup.short_pitch
