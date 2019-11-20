import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger()


class TrackAPICalls(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request, 'user', None)

        user_email = getattr(user, 'email', None)

        data = {
            'user': user_email,
            'path': request.path,
            'uri': request.build_absolute_uri(),
            'is_ajax': request.is_ajax(),
        }
        logger.info(data)
        return
