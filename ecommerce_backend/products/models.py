from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Product name"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed product description"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Product price (must be positive)"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Available quantity in stock"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when product was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save(update_fields=['stock'])
            return True
        return False
    
    def increase_stock(self, quantity):
       
        self.stock += quantity
        self.save(update_fields=['stock'])