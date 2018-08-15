import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from impact.graphql.types.expert_profile_type import ExpertProfileType
from accelerator.models.expert_profile import ExpertProfile
from accelerator_abstract.models.base_base_profile import (
    EXPERT_USER_TYPE,
)


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(ExpertProfileType, id=graphene.Int())

    def resolve_expert_profile(self, info, **kwargs):
        user_id = kwargs.get('id')

        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
            if user.get_profile().user_type.upper() == EXPERT_USER_TYPE:
                return ExpertProfile.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return None

        return None
