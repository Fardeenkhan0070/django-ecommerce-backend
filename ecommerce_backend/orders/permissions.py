

from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
   
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
       
        # Admin can access all orders
        if request.user.is_staff:
            return True
        
        # Regular users can only access their own orders
        return obj.user == request.user