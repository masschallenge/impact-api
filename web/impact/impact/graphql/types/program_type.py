import graphene

from graphene_django import DjangoObjectType

from accelerator.models import Program


class ProgramType(DjangoObjectType):
    year = graphene.String()
    family = graphene.String()

    class Meta:
        model = Program
        only_fields = (
            'name',
        )

    def resolve_year(self, info, **kwargs):
        if self.start_date:
            return self.start_date.year

        return ''

    def resolve_family(self, info, **kwargs):
        return self.program_family.name
