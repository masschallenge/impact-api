import graphene

from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from accelerator_abstract.models.base_user_utils import is_employee

from mc.utils import swapper_model
from ..auth.utils import can_view_private_data

ExpertProfile = swapper_model('ExpertProfile')
User = get_user_model()


class UserType(DjangoObjectType):
    is_staff = graphene.Boolean()

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

    def resolve_is_staff(self, info, **kwargs):
        return is_employee(self)
