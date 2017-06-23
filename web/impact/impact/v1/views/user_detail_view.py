from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from simpleuser.models import USER_KEY_TRANSLATIONS
from impact.permissions import (
    V1APIPermissions,
)
from impact.utils import user_gender


User = get_user_model()


class UserDetailView(APIView):
    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        result = {
            "id": pk,
            "first_name": user.full_name,
            "last_name": user.short_name,
            "email": user.email,
            "is_active": user.is_active,
            "gender": user_gender(user),
            }
        return Response(result)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        data = request.data
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, data[key])
            else:
                alt_key = USER_KEY_TRANSLATIONS.get(key)
                if alt_key:
                    setattr(user, alt_key, data[key])
        user.save()
        return Response(status=200)
