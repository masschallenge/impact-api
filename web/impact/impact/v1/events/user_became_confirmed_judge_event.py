from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)

class UserBecameConfirmedJudgeEvent(BaseUserRoleGrantEvent):
    DESCRIPTION_FORMAT = "Became Confirmed Judge for {name} ({id})"
    EVENT_TYPE = "became confirmed judge"
    USER_ROLE = UserRole.JUDGE

    def description():
        judging_round = 
        return self.DESCRIPTION_FORMAT.format(
                                        name=judging_round.short_name(),
                                        id=judging_round.id)

    def _confirmed_judge_datetime(self):
        program = self.program_role_grant.program_role.program 
        result = program.judginground_set.first().created_at
        if result is None:
            return program.start_date
        return result
