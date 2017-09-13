from impact.models import BaseProfile


class UserHelper(object):
    def __init__(self, user):
        self.user = user

    def serialize(self):
        return {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.full_name,
            "last_name": self.user.short_name,
            "is_active": self.user.is_active,
            "gender": self.user_gender(),
            'updated_at': self._get_profile_update_timestamp(),
            "last_login": self.user.last_login,
            }

    def get_profile(self):
        try:
            user_type = self.user.baseprofile.user_type
            if user_type == "ENTREPRENEUR":
                return self.user.entrepreneurprofile
            if user_type == "EXPERT":
                return self.user.expertprofile
            return self.user.memberprofile
        except BaseProfile.DoesNotExist:
            return None

    def _get_profile_update_timestamp(self):
        profile = self.get_profile()
        if profile:
            return profile.updated_at
        return None

    def user_gender(self):
        profile = self.get_profile()
        if profile:
            return profile.gender
        return None
