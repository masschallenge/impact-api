from datetime import timedelta

from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from accelerator_abstract.models.base_user_utils import is_employee
from accelerator.models import (
    Clearance,
    MentorProgramOfficeHour,
    UserRole
)
from .location_serializer import LocationSerializer
from .user_serializer import UserSerializer

INVALID_END_DATE = 'office hour end time must be later than the start time'
INVALID_USER = ('must have clearance or be of type Mentor or Alumni in '
                'residence in an active program')
INVALID_SESSION_DURATION = 'Please specify a duration of 30 minutes or more.'
THIRTY_MINUTES = timedelta(minutes=30)
NO_START_DATE_TIME = "start_date_time must be specified"
NO_END_DATE_TIME = "end_date_time must be specified"
CONFLICTING_SESSIONS = "There are conflicts with existing office hours"


class OfficeHourSerializer(ModelSerializer):
    class Meta:
        model = MentorProgramOfficeHour
        fields = [
            'id', 'mentor', 'start_date_time', 'end_date_time',
            'topics', 'description', 'location', 'meeting_info'
        ]

    def handle_conflicting_session(self, attrs, start_time, end_time):
        mentor = attrs.get('mentor', None) or self.instance.mentor
        start_conflict = (Q(start_date_time__gt=start_time) &
                          Q(start_date_time__lt=end_time))
        end_conflict = (Q(end_date_time__gt=start_time) &
                        Q(end_date_time__lt=end_time))
        enclosing_conflict = (Q(start_date_time__lte=start_time) &
                              Q(end_date_time__gte=end_time))
        conflict = mentor.mentor_officehours.filter(
            start_conflict | end_conflict | enclosing_conflict
        ).exists()
        if conflict:
            raise ValidationError({
                'start_date_time': CONFLICTING_SESSIONS})

    def validate_office_hour_session(self, attrs):
        office_hour = self.instance
        start_time = attrs.get('start_date_time', None)
        end_time = attrs.get('end_date_time', None)
        skip_check = (office_hour and
                      (office_hour.start_date_time == start_time and
                       office_hour.end_date_time == end_time))
        if (start_time or end_time) and not skip_check:
            self.handle_conflicting_session(attrs, start_time, end_time)

    def validate(self, attrs):
        start_date_time = None
        end_date_time = None
        if self.instance is not None:
            start_date_time = self.instance.start_date_time
            end_date_time = self.instance.end_date_time

        start_date_time = attrs.get('start_date_time') or start_date_time
        end_date_time = attrs.get('end_date_time') or end_date_time
        if not start_date_time:
            raise ValidationError({
                'start_date_time': NO_START_DATE_TIME})
        if not end_date_time:
            raise ValidationError({
                'end_date_time': NO_END_DATE_TIME})

        if start_date_time > end_date_time:
            raise ValidationError({
                'end_date_time': INVALID_END_DATE})
        if end_date_time - start_date_time < THIRTY_MINUTES:
            raise ValidationError({
                'end_date_time': INVALID_SESSION_DURATION})
        self.validate_office_hour_session(attrs)

        return attrs

    def is_allowed_mentor(self, mentor):
        user = self.context['request'].user
        roles = [UserRole.MENTOR, UserRole.AIR]
        if user == mentor:
            return Clearance.objects.clearances_for_user(user).filter(
                program_family__programs__program_status='active').exists()
        return mentor.programrolegrant_set.filter(
            program_role__user_role__name__in=roles,
            program_role__program__program_status='active',
        ).exists()

    def validate_mentor(self, mentor):
        user = self.context['request'].user
        if not is_employee(user):
            return user
        if not self.is_allowed_mentor(mentor):
            raise ValidationError(INVALID_USER)
        return mentor

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['mentor'] = UserSerializer(instance.mentor).data
        data['location'] = LocationSerializer(instance.location).data
        return data
