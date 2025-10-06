from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .models import Book

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.
    """
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for managing books.
    """
    list_display = ['title', 'author', 'isbn', 'publication_date', 'created_by', 'created_at']
    list_filter = ['author', 'publication_date', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn')
        }),
        ('Details', {
            'fields': ('publication_date', 'description')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Automatically set the created_by field to the current user when creating a new book.
        """
        if not change:  # If this is a new object (not being edited)
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(CustomUser, CustomUserAdmin)