from rest_framework.permissions import BasePermission
from common.constants import SELLERS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name=SELLERS).exists()
        )
