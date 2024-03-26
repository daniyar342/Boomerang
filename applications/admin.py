from django.contrib import admin
from django.http import HttpRequest
from .models import Cart,Order

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'product_name']  # Замените 'product' на 'product_name'

    def get_user(self, obj):
        return obj.user.email_or_phone if obj.user else "Unknow"

    def product_name(self, obj):
        return obj.product.name if obj.product else "Unknown"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
                'date',
                'status',
                'address',
                'cart_product',
                ]