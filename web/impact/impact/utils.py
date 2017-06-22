# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


def compose_filter(key_pieces, value):
    return {"__".join(key_pieces): value}


def get_profile(user):
    user_type = user.baseprofile.user_type
    if user_type == "ENTREPRENEUR":
        return user.entrepreneurprofile
    if user_type == "EXPERT":
        return user.expertprofile
    return user.memberprofile
