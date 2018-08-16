import graphene

from impact.graphql.types.expert_profile_type import ExpertProfileType
from accelerator.models.expert_profile import ExpertProfile


class Query(graphene.ObjectType):
    expert_profile = graphene.Field(ExpertProfileType, id=graphene.Int())

    def resolve_expert_profile(self, info, **kwargs):
        user_id = kwargs.get('id')

        if user_id is not None:
            return ExpertProfile.objects.get(user_id=user_id)

        return None
