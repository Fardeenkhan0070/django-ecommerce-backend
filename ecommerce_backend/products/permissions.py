"""
File: products/permissions.py
Purpose: Custom permission classes for product management
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Read permissions (GET, HEAD, OPTIONS) are allowed to any user
    - Write permissions (POST, PUT, PATCH, DELETE) are only allowed to admin/staff users
    
    This ensures:
    - Anyone can VIEW products
    - Only admin/staff can CREATE, UPDATE, DELETE products
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to authenticated staff/admin users
        return request.user and request.user.is_authenticated and request.user.is_staff