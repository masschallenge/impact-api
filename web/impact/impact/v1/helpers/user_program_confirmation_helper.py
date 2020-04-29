from accelerator.models import User, UserRole
from impact.v1.helpers.model_helper import (
    ModelHelper,
    READ_ONLY_OBJECT_FIELD,
)

USER_FIELDS = {
    'program_participation': READ_ONLY_OBJECT_FIELD,
}


class UserProgramConfirmationHelper(ModelHelper):
    model = User

    @classmethod
    def fields(cls):
        return USER_FIELDS

    def get_user_program_participation_for_role(self, user_role=None):
        return list(
            self.subject.programrolegrant_set.filter(
                program_role__user_role__name=user_role,
            ).values_list('program_role__program', flat=True).distinct())

    @property
    def program_participation(self):
        return {
            'deferred': self.get_user_program_participation_for_role(
                UserRole.DEFERRED_MENTOR),
            'confirmed': self.get_user_program_participation_for_role(
                UserRole.MENTOR)
        }
