from django.contrib.auth import get_user_model
from django.template import loader
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from accelerator.models import (
    UserRole,
    Program,
    ProgramRoleGrant,
    ProgramRole
)
from impact.minimal_email_handler import MinimalEmailHandler
from impact.v1.helpers import UserProgramConfirmationHelper
from impact.v1.views.base_detail_view import BaseDetailView
from impact.v1.views.user_detail_view import NO_USER_ERROR

from impact.permissions.v1_api_permissions import UserDetailViewPermission

User = get_user_model()

SUBJECT = '[MassChallenge] Confirmed: Your Mentorship Commitment'
MENTOR_SHIP_COMMITMENT_EMAIL_TEMPLATE = 'emails/mentorship_commitment_email.html'
INVALID_INPUT_ERROR = "'{}' must be a list of numbers."


def validate_input(request, key):
    try:
        return list(map(int, request.data.get(key, [])))
    except Exception:
        raise ParseError(INVALID_INPUT_ERROR.format(key))


class UserProgramConfirmationDetailView(BaseDetailView):
    view_name = "user_program_confirmation_detail"
    helper_class = UserProgramConfirmationHelper
    permission_classes = (UserDetailViewPermission,)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def add_programrolegrant(self, program_ids=None, user_role=None):
        programs = Program.objects.filter(pk__in=program_ids)
        user_role_obj = UserRole.objects.get(name=user_role)

        programrolegrants = [
            ProgramRoleGrant(
                person=self.user,
                program_role=ProgramRole.objects.filter(
                    program=program,
                    user_role=user_role_obj
                ).first())
            for program in programs
        ]
        ProgramRoleGrant.objects.bulk_create(
            programrolegrants,
            ignore_conflicts=True
        )

    def update_user_confirmation(self, delete_user_role, add_user_role, program_ids=None):
        self.user.programrolegrant_set.filter(
            program_role__program__in=program_ids,
            program_role__user_role__name=delete_user_role
        ).delete()
        self.add_programrolegrant(program_ids=program_ids, user_role=add_user_role)

    def post(self, request, pk):
        self.user = User.objects.filter(pk=pk).first()
        if not self.user:
            return Response(status=404, data=NO_USER_ERROR.format(pk))
        deferred_programs = validate_input(request, 'deferred')
        confirmed_programs = validate_input(request, 'confirmed')

        if deferred_programs:
            self.update_user_confirmation(
                UserRole.MENTOR, UserRole.DEFERRED_MENTOR, deferred_programs)
        if confirmed_programs:
            self.update_user_confirmation(
                UserRole.DEFERRED_MENTOR, UserRole.MENTOR, confirmed_programs)
            self.send_email()
        return Response({'success': True})

    def send_email(self):
        context = {
            'mentor_first_name': self.user.first_name,
            'confirmed_programs': Program.objects.filter(
                pk__in=self.user.programrolegrant_set.filter(
                    program_role__user_role__name=UserRole.MENTOR
                ).values_list('program_role__program__pk', flat=True)
            )
        }
        html_email = loader.render_to_string(
            MENTOR_SHIP_COMMITMENT_EMAIL_TEMPLATE,
            context
        )
        MinimalEmailHandler(
            to=[self.user.email],
            body=None,
            subject=SUBJECT,
            attach_alternative=[html_email, 'text/html']
        ).send()
