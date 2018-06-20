from graphene_django import DjangoObjectType

from accelerator.models.startup import Startup


class StartupType(DjangoObjectType):
    class Meta:
        model = Startup
        only_fields = ('short_pitch',)
