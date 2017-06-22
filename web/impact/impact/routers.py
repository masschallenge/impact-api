# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


class APIRouter(object):

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure that we don't migrate
        apps shared by both accelerate and impact
        """
        if app_label in [
                'auth',
                'admin',
                'sessions',
                'sites',
                'contenttypes']:
            return False
        return True
