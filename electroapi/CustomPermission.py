from rest_framework import permissions

class IsGetOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        else:
            return False