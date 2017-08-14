from factory import (
    DjangoModelFactory,
    SubFactory,
)
from impact.tests.factories.user_factory import UserFactory
from impact.tests.factories.program_family_factory import ProgramFamilyFactory
from impact.models import (
    Clearance,
    CLEARANCE_LEVEL_POM,
)


class ClearanceFactory(DjangoModelFactory):
    class Meta:
        model = Clearance

    user = SubFactory(UserFactory)
    program_family = SubFactory(ProgramFamilyFactory)
    level = CLEARANCE_LEVEL_POM
