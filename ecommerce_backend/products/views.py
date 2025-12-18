"""
File: products/views.py
Purpose: ViewSet for handling Product CRUD operations
"""

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations.
    
    Provides:
    - list: GET /api/products/ - List all products
    - retrieve: GET /api/products/<id>/ - Get single product
    - create: POST /api/products/ - Create new product (admin only)
    - update: PUT /api/products/<id>/ - Update product (admin only)
    - partial_update: PATCH /api/products/<id>/ - Partial update (admin only)
    - destroy: DELETE /api/products/<id>/ - Delete product (admin only)
    
    Features:
    - Pagination (configured in settings)
    - Filtering by price and stock
    - Searching by name and description
    - Ordering by any field
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    # Fields that can be filtered
    filterset_fields = {
        'price': ['exact', 'gte', 'lte'],  # ?price=10 or ?price__gte=10 or ?price__lte=100
        'stock': ['exact', 'gte', 'lte'],  # ?stock=0 or ?stock__gte=5
    }
    
    # Fields that can be searched (bonus feature)
    search_fields = ['name', 'description']  # ?search=laptop
    
    # Fields that can be used for ordering (bonus feature)
    ordering_fields = ['name', 'price', 'stock', 'created_at']  # ?ordering=-price
    ordering = ['-created_at']  # Default ordering
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view,
        full serializer for detail view.
        """
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new product (admin only).
        POST /api/products/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {
                'message': 'Product created successfully',
                'product': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a product (admin only).
        PUT /api/products/<id>/
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Product updated successfully',
                'product': serializer.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a product (admin only).
        DELETE /api/products/<id>/
        """
        instance = self.get_object()
        product_name = instance.name
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Product "{product_name}" deleted successfully'
            },
            status=status.HTTP_200_OK
        )