from rest_framework.permissions import BasePermission
from common.constants import BUYERS


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name=BUYERS).exists()
        )
