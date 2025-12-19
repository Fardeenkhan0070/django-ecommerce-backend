"""
File: orders/models.py
Purpose: Order and OrderItem models for e-commerce system
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from products.models import Product


class Order(models.Model):
    """
    Order model representing a customer's purchase.
    Contains order status, total amount, and references to user.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="User who placed the order"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        help_text="Current order status"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total order amount"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when order was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.get_subtotal() for item in self.items.all())
        return total
    
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']


class OrderItem(models.Model):
    """
    OrderItem model representing individual products in an order.
    This is a through table connecting Order and Product.
    """
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Order this item belongs to"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,  # Don't allow deleting products that are in orders
        related_name='order_items',
        help_text="Product being ordered"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of product ordered"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price at time of purchase (snapshot)"
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ['order', 'product']  # Prevent duplicate products in same order
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        """Override save to capture current price if not set"""
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)