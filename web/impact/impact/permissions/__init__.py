from django.conf import settings
from rest_framework.permissions import BasePermission
from impact.permissions.permissions_utils import (
    global_operations_manager_check)
from impact.permissions.directory_access_permissions import (
    DirectoryAccessPermissions,
)
from impact.permissions.v1_confidential_api_permissions import (
    V1ConfidentialAPIPermissions,
)
from impact.permissions.v1_api_permissions import (
    V1APIPermissions
)
from impact.permissions.v0_api_permissions import (
    V0APIPermissions
)
from impact.permissions.dynamic_model_permissions import (
    DynamicModelPermissions
)
from impact.permissions.allocate_applications_permissions import (
    AllocateApplicationsPermissions
)