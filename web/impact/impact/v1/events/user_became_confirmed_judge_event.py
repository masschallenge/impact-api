from impact.models import UserRole
from impact.utils import compose_filter


class UserBecameConfirmedJudgeEvent(object):
    DESCRIPTION_FORMAT = "Became Confirmed Judge for {name} ({id})"
    EVENT_TYPE = "became confirmed judge"

    def __init__(self, program_role_grant):
        self.program_role_grant = program_role_grant

    @classmethod
    def events(cls, user):
        result = []
        for prg in user.programrolegrant_set.filter(**compose_filter(
            ["program_role",
            "user_role",
            "name"],
            UserRole.JUDGE)):
            result.append(cls(prg))
        return result

    def serialize(self):
        confirmed_judge_time = self._confirmed_judge_datetime()
        program = self.program_role_grant.program_role.program
        judging_round = program.judginground_set.first()
        return {
            "datetime": confirmed_judge_time,
            "latest_datetime": "",
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                name=judging_round.short_name(),
                id=judging_round.id)
            }

    def _confirmed_judge_datetime(self):
        program = self.program_role_grant.program_role.program 
        result = program.judginground_set.first().created_at
        if result is None:
            return program.start_date
        return result
