from django.contrib.auth import get_user_model
from django.db.models import F
from django.template import loader
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from accelerator.models import (
    UserRole,
    Program,
    ProgramRoleGrant,
    ProgramRole
)
from .minimal_email_handler import MinimalEmailHandler
from .permissions.v1_api_permissions import IsExpertUser
from .v1.views import ImpactView
from .v1.views.user_detail_view import NO_USER_ERROR

User = get_user_model()

SUBJECT = '[MassChallenge] Confirmed: Your Mentorship Commitment'
INVALID_INPUT_ERROR = "'{}' must be a list of numbers."


def extract_values(request, key):
    try:
        return [int(i) for i in request.data.get(key, [])]
    except ValueError:
        raise ParseError(INVALID_INPUT_ERROR.format(key))


class MentorParticipationView(ImpactView):
    view_name = "mentor_participation_view"
    permission_classes = (IsExpertUser,)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def add_program_role_grants(self, program_ids=None, user_role=None):
        programs = Program.objects.filter(pk__in=program_ids)
        program_roles = dict(ProgramRole.objects.filter(
            user_role__name=user_role
        ).order_by('-id').values_list('program_id', 'id'))
        program_role_grants = [
            ProgramRoleGrant(
                person=self.user,
                program_role_id=program_roles[program.id]
            )
            for program in programs
        ]
        ProgramRoleGrant.objects.bulk_create(
            program_role_grants,
            ignore_conflicts=True
        )

    def delete_program_role_grants(self, program_ids=None, user_role=None):
        self.user.programrolegrant_set.filter(
            program_role__program__in=program_ids,
            program_role__user_role__name=user_role
        ).delete()

    def handle_user_confirmation(self, delete_roles, add_roles, program_ids):
        self.delete_program_role_grants(program_ids, delete_roles)
        self.add_program_role_grants(program_ids, add_roles)

    def post(self, request):
        user_id = request.user.id
        self.user = User.objects.filter(pk=user_id).first()
        if not self.user:
            return Response(status=404, data=NO_USER_ERROR.format(user_id))
        deferred_programs = extract_values(request, 'deferred')
        confirmed_programs = extract_values(request, 'confirmed')
        success = False
        if deferred_programs:
            self.handle_user_confirmation(
                UserRole.MENTOR, UserRole.DEFERRED_MENTOR, deferred_programs)
            success = True
        if confirmed_programs:
            self.handle_user_confirmation(
                UserRole.DEFERRED_MENTOR, UserRole.MENTOR, confirmed_programs)
            self.send_email(confirmed_programs)
            success = True
        return Response({'success': success})

    def send_email(self, confirmed_programs):
        program_data = self.user.programrolegrant_set.filter(
            program_role__user_role__name=UserRole.MENTOR,
            program_role__program__id__in=confirmed_programs,
        ).values(
            start_date=F('program_role__program__start_date'),
            end_date=F('program_role__program__end_date'),
            name=F('program_role__program__name'),
        )
        context = {
            'mentor_first_name': self.user.first_name,
            'confirmed_programs': program_data
        }
        html_email = loader.render_to_string(
            'emails/mentorship_commitment_email.html',
            context
        )
        MinimalEmailHandler(
            to=[self.user.email],
            body=None,
            subject=SUBJECT,
            attach_alternative=[html_email, 'text/html']
        ).send()
