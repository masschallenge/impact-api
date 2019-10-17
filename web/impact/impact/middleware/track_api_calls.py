import logging

logger = logging.getLogger(__file__)


class TrackAPICalls(object):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user:
            user_email = user.email
        else:
            user_email = None

        data = {
            'user': user_email,
            'path': request.path,
            'uri': request.build_absolute_uri,
            'is_ajax': request.is_ajax(),
        }
        logger.info(data)
        return
