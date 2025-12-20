
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCancelSerializer
)
from .permissions import IsOrderOwner


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order operations.
    
    Provides:
    - list: GET /api/orders/ - List user's own orders
    - retrieve: GET /api/orders/<id>/ - Get order details (own orders only)
    - create: POST /api/orders/ - Create new order with items
    - cancel: POST /api/orders/<id>/cancel/ - Cancel order (BONUS)
    
    Features:
    - Users can only view their own orders
    - Stock validation during order creation
    - Automatic stock deduction
    - Order cancellation with stock rollback
    - Optimized queries with prefetch_related
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    
    def get_queryset(self):
        """
        Return orders for the current user only.
        Staff/admin can see all orders.
        Optimized with prefetch_related to reduce queries.
        """
        user = self.request.user
        
        # Optimize query by prefetching related items and products
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product')
            )
        ).select_related('user')
        
        # Filter by user (unless staff/admin)
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'cancel':
            return OrderCancelSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new order with items.
        POST /api/orders/
        
        Request body:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 3, "quantity": 1}
            ]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return the created order with full details
        output_serializer = OrderSerializer(order)
        
        return Response(
            {
                'message': 'Order created successfully',
                'order': output_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get order details.
        GET /api/orders/<id>/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        """
        List all orders for the authenticated user.
        GET /api/orders/
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order and restore stock (BONUS FEATURE).
        POST /api/orders/<id>/cancel/
        
        Only pending or confirmed orders can be cancelled.
        Stock is automatically restored.
        """
        order = self.get_object()
        
        serializer = self.get_serializer(order, data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated order
        output_serializer = OrderSerializer(order)
        
        return Response(
            {
                'message': 'Order cancelled successfully',
                'order': output_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    # Disable update and delete for orders (business rule)
    def update(self, request, *args, **kwargs):
        """Orders cannot be updated, only cancelled"""
        return Response(
            {'detail': 'Orders cannot be updated. Use cancel endpoint instead.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """Orders cannot be deleted"""
        return Response(
            {'detail': 'Orders cannot be deleted. Use cancel endpoint instead.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )