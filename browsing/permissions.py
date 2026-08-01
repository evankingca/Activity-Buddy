from rest_framework.permissions import BasePermission

class IsSelf(BasePermission):
    """
    Allows access only to the user themselves.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsConnectionUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.user_a, obj.user_b]

