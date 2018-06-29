from graphql_jwt.shortcuts import get_user_by_token

from impact.graphql.auth.utils import get_jwt_cookie


class JWTokenCookieBackend(object):

    def authenticate(self, request=None, **credentials):
        if request is None:
            return None
        token = get_jwt_cookie(request)
        if token is not None:
            user = get_user_by_token(token)
            return user
        return None
