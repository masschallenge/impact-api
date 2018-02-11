# MIT License
# Copyright (c) 2017 MassChallenge, Inc.
from multidb import MasterSlaveRouter


class ImpactRouter(object):

    def allow_migrate(
            self,
            db,
            app_label,
            model_name=None,
            **hints):
        """
        Make sure that we don't migrate
        apps shared by both accelerate and impact
        """
        if app_label in [
                'auth',
                'admin',
                'sessions',
                'simpleuser',
                'sites',
                'contenttypes']:
            return False
        return True


class MasterSlaveAPIRouter(MasterSlaveRouter):

    def allow_migrate(
            self,
            db,
            app_label,
            model_name=None,
            **hints):
        """
        Make sure that we don't migrate
        apps shared by both accelerate and impact
        """
        allow_migrate = super().allow_migrate(
            db, app_label,
            model_name,
            **hints)

        if app_label in [
                'auth',
                'admin',
                'sessions',
                'simpleuser',
                'sites',
                'contenttypes']:
            return False
        return allow_migrate
