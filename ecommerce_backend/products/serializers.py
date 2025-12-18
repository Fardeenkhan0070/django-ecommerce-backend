"""
File: products/serializers.py
Purpose: Serializers for Product model with validation
"""

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Handles validation and conversion between Product model and JSON.
    """
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'is_in_stock',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_stock(self, value):
        """Ensure stock is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
    
    def validate_name(self, value):
        """Ensure product name is not empty or just whitespace"""
        if not value or not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value.strip()


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing products.
    Excludes description for better performance.
    """
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'is_in_stock', 'created_at']
        read_only_fields = ['id', 'created_at']