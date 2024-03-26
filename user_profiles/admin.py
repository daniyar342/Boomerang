from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(CustomUser)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "email_or_phone", "is_active", ]
    list_filter = ["is_active"]
    search_fields = ["username"]
