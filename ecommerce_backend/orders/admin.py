from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
   
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'get_subtotal']
    fields = ['product', 'quantity', 'price', 'get_subtotal']
    
    def get_subtotal(self, obj):
       
        if obj.id:
            return f"${obj.get_subtotal()}"
        return "-"
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   
    list_display = ['id', 'user', 'status', 'total_amount', 'item_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def item_count(self, obj):
        
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def has_delete_permission(self, request, obj=None):
        
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
   
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'get_subtotal']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['price', 'get_subtotal']
    
    def get_subtotal(self, obj):
        """Display subtotal"""
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'