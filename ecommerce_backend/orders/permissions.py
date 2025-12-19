"""
File: orders/permissions.py
Purpose: Custom permissions for order management
"""

from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to ensure users can only access their own orders.
    
    As per PDF requirement: "Users can only view their own orders"
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the order belongs to the requesting user.
        Staff/admin users can access all orders.
        """
        # Admin can access all orders
        if request.user.is_staff:
            return True
        
        # Regular users can only access their own orders
        return obj.user == request.user