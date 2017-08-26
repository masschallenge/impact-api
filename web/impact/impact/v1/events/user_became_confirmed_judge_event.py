from impact.models import UserRole
from impact.v1.events.base_user_role_grant_event import (
    BaseUserRoleGrantEvent,
)


class UserBecameConfirmedJudgeEvent(BaseUserRoleGrantEvent):
    PROGRAM_ROLE_FORMAT = "Granted Confirmed Judge Program Role {name} ({id})"
    JUDGING_ROUND_FORMAT = "Confirmed as Judge for Judging Round {name} ({id})"
    EVENT_TYPE = "became confirmed judge"
    USER_ROLE = UserRole.JUDGE

    def description(self):
        program_role = self.program_role_grant.program_role
        label = program_role.user_label
        if label:
            judging_round = label.rounds_confirmed_for.first()
            if judging_round:
                return self.JUDGING_ROUND_FORMAT.format(
                    name=judging_round.short_name(),
                    id=judging_round.id)
        return self.PROGRAM_ROLE_FORMAT.format(
            name=program_role.name,
            id=program_role.id)
