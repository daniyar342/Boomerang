from django.contrib import admin
from .models import Product,Category,Recall,ProductImage


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = "title".split()


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = "get_user_email product rating text".split()
    list_filter = ['rating']

    def get_user_email(self, obj):
        return obj.user.email_or_phone if obj.user else "Unknown"


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_user_email', 'slug', 'price', 'available', 'created', 'updated')
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    inlines = [ProductImageInline]

    def get_user_email(self, obj):
        return obj.user.email_or_phone if obj.user else "Unknown"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
    

