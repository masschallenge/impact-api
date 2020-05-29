from graphql_jwt.exceptions import GraphQLJWTError
from graphql_jwt.middleware import JSONWebTokenMiddleware

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .utils import get_jwt_cookie


class CookieJSONWebTokenMiddleware(JSONWebTokenMiddleware, MiddlewareMixin):

    def process_request(self, request):
        if get_jwt_cookie(request) is None:
            return None
        if hasattr(request, 'user') and not request.user.is_anonymous:
            return None
        try:
            user = authenticate(request=request)
        except GraphQLJWTError as err:
            return JsonResponse({'errors': [{'message': str(err)}], },
                                status=401)
        if user is not None:
            request.user = request._cached_user = user
