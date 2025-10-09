from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'bio', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)