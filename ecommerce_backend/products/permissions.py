from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
           return True
        
        # Write permissions are only allowed to authenticated staff/admin users
        return request.user and request.user.is_authenticated and request.user.is_staff