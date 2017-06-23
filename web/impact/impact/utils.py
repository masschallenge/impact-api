# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from impact.models import BaseProfile


def compose_filter(key_pieces, value):
    return {"__".join(key_pieces): value}


def get_profile(user):
    try:
        user_type = user.baseprofile.user_type
        if user_type == "ENTREPRENEUR":
            return user.entrepreneurprofile
        if user_type == "EXPERT":
            return user.expertprofile
        return user.memberprofile
    except BaseProfile.DoesNotExist:
        return None


def user_gender(user):
    profile = get_profile(user)
    if profile:
        return profile.gender
    return None
