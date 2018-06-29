from graphql import GraphQLError

NOT_LOGGED_IN_MSG = 'User Not Logged in!'


class IsAuthenticatedMiddleware(object):
    def resolve(self, next, root, info, **args):
        if not info.context.user.is_authenticated():
            raise GraphQLError(NOT_LOGGED_IN_MSG)
        return next(root, info, **args)
