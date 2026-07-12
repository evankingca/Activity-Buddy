from rest_framework.permissions import BasePermission

class IsSelf(BasePermission):
    """
    Allows access only to the user themselves.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
