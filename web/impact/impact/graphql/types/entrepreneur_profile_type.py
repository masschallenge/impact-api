import graphene
from graphene_django import DjangoObjectType
from accelerator.models import EntrepreneurProfile


class EntrepreneurProfileType(DjangoObjectType):
    image_url = graphene.String()
    current_program = graphene.String()

    class Meta:
        model = EntrepreneurProfile
        only_fields = (
            'facebook_url',
            'linked_in_url',
            'personal_website_url',
            'phone',
            'twitter_handle',
        )

    def resolve_image_url(self, info, **kwargs):
        return self.image and self.image.url

    def resolve_current_program(self, info, **kwargs):
        return self.current_program.name
