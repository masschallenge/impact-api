import graphene
import graphql_jwt

from .query import Query as BaseQuery


class Query(BaseQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema(query=Query)
auth_schema = graphene.Schema(mutation=Mutation)
