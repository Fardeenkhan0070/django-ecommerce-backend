
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
   
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    
    def get_queryset(self):
        
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
    
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'cancel':
            return OrderCancelSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        
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
       
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        
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
       
        return Response(
            {'detail': 'Orders cannot be updated. Use cancel endpoint instead.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
       
        return Response(
            {'detail': 'Orders cannot be deleted. Use cancel endpoint instead.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )