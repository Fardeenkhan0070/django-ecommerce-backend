"""
File: orders/serializers.py
Purpose: Serializers for Order and OrderItem with nested structure and validation
"""

from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem (nested in orders).
    Shows product details and calculates subtotal.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        source='get_subtotal'
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price', 'subtotal']
    
    def validate_quantity(self, value):
        """Ensure quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Serializer for creating order items (used in order creation).
    Only requires product ID and quantity.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        """Validate that product exists"""
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with ID {value} does not exist.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Order details with nested items.
    Read-only, used for retrieving order information.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_email',
            'status',
            'total_amount',
            'items',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating new orders.
    Accepts a list of items with product_id and quantity.
    Handles stock validation and order creation with transaction.
    """
    items = OrderItemCreateSerializer(many=True)
    
    def validate_items(self, value):
        """Validate that items list is not empty"""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
    
    def validate(self, data):
        """
        Validate stock availability for all items.
        This runs before create() to ensure all products have sufficient stock.
        """
        items = data.get('items', [])
        
        for item_data in items:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product with ID {product_id} does not exist."
                )
            
            # Check stock availability
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{product.name}'. "
                    f"Available: {product.stock}, Requested: {quantity}"
                )
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
       
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Create the order (total_amount will be calculated)
        order = Order.objects.create(
            user=user,
            total_amount=0  # Will be updated after adding items
        )
        
        total_amount = 0
        
        # Create order items and deduct stock
        for item_data in items_data:
            product = Product.objects.select_for_update().get(id=item_data['product_id'])
            quantity = item_data['quantity']
            
            # Double-check stock (in case of concurrent requests)
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{product.name}'."
                )
            
            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price  # Capture current price
            )
            
            # Deduct stock (BONUS FEATURE)
            product.reduce_stock(quantity)
            
            # Add to total
            total_amount += order_item.get_subtotal()
        
        # Update order total
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])
        
        return order


class OrderCancelSerializer(serializers.Serializer):
  
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cancel order and restore stock.
        """
        if not instance.can_be_cancelled():
            raise serializers.ValidationError(
                f"Order with status '{instance.status}' cannot be cancelled."
            )
        
        # Restore stock for all items
        for item in instance.items.select_related('product'):
            product = Product.objects.select_for_update().get(id=item.product.id)
            product.increase_stock(item.quantity)
        
        # Update order status
        instance.status = 'cancelled'
        instance.save(update_fields=['status'])
        
        return instance