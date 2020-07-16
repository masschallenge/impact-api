from accelerator.models import ExpertProfile
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from ...graphql.auth.utils import can_view_private_data

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'first_name', 'last_name', 'email')

    def resolve_email(self, info, **kwargs):
        profile = self.get_profile()
        email = self.email
        if type(profile) is ExpertProfile:
            if not can_view_private_data(info.context.user, profile.privacy_email):
                email = ""
        return email
