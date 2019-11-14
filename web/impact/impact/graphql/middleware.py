from django.utils.deprecation import MiddlewareMixin

from impact.graphql.utils.response_error import ResponseError


NOT_LOGGED_IN_MSG = 'User Not Logged in!'


class IsAuthenticatedMiddleware(MiddlewareMixin):
    def resolve(self, next, root, info, **args):
        if not info.context.user.is_authenticated:
            raise ResponseError(message=NOT_LOGGED_IN_MSG, code="401")
        return next(root, info, **args)
