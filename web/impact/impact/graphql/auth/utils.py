from django.conf import settings


def get_jwt_cookie(request):
    cookie_name = settings.JWT_AUTH.get('JWT_AUTH_COOKIE')
    if cookie_name:
        return request.COOKIES.get(cookie_name)
    return None
