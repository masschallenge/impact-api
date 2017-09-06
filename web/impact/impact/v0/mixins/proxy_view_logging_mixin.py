from django.utils.timezone import now
from rest_framework_tracking.models import APIRequestLog


class LogProxyView():
    """
    Manual logging for proxy views, which can't use the drf-tracking mixin.
    """

    def log(self):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR")
        ip = ip or self.request.META.get("REMOTE_ADDR")
        logline = APIRequestLog(
            host=self.request.get_host(),
            method=self.request.method,
            path=self.request.path,
            query_params=self.request.query_params.dict(),
            remote_addr=ip,
            requested_at=now(),
        )
        logline.save()
