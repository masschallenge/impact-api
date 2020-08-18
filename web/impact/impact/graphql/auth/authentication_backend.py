from graphql_jwt.utils import get_user_by_payload
from graphql_jwt.exceptions import GraphQLJWTError
from mc_sso.jwt_utils import (
    get_payload_from_token,
    get_token_from_request,
)


class JWTokenCookieBackend(object):

    def authenticate(self, request=None, **credentials):
        if request is None:
            return None
        token = get_token_from_request(request)
        payload = get_payload_from_token(token)
        if payload:
            try:
                user = get_user_by_payload(payload)
                return user
            except GraphQLJWTError:
                return None
        return None
