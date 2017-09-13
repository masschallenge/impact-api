from impact.models import BaseProfile


class UserHelper(object):
    def __init__(self, user):
        self.user = user

    def serialize(self):
        return {
            "id": self.user.id,
            'updated_at': self._get_profile_update_timestamp(),
            "last_login": self.user.last_login,
            "date_joined": self.user.date_joined,
            "email": self.user.email,
            "first_name": self.user.full_name,
            "last_name": self.user.short_name,
            "is_active": self.user.is_active,
            "gender": self.gender(),
            "phone": self.phone(),
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

    def gender(self):
        profile = self.get_profile()
        if profile:
            return profile.gender
        return None

    def phone(self):
        profile = self.get_profile()
        if profile:
            return profile.phone
        return None
