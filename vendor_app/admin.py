from django.contrib import admin
from .models import (
    Category, Product, ProductVariant, Customer, 
    Order, OrderItem, Cart, CartItem
)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'hair_type', 'stock')
    list_filter = ('category', 'hair_type')
    search_fields = ('name', 'description')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'total_amount')
    list_filter = ('status',)
    search_fields = ('customer__user__username',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
