import graphene
import graphql_jwt

from . import query


class Query(impact.graphql.query.Query, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema(query=Query)
auth_schema = graphene.Schema(mutation=Mutation)
