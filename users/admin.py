from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active']
    list_editable = ['is_active']
admin.site.register(CustomUser, CustomUserAdmin)