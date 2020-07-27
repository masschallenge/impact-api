from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from mc.utils import swapper_model
from ..auth.utils import can_view_private_data

ExpertProfile = swapper_model('ExpertProfile')
User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'first_name', 'last_name', 'email')

    def resolve_email(self, info, **kwargs):
        profile = self.get_profile()
        email = self.email
        request_user = info.context.user
        if type(profile) is ExpertProfile:
            if not can_view_private_data(request_user, profile.privacy_email):
                email = ""
        return email
