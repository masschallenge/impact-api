# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.api_data import APIData


class StartupDetailData(APIData):

    def valid(self):
        self.program = self.validate_program(required=False)
        self.startup = self.validate_startup()
        return self.errors == []
