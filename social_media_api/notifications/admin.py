from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['actor', 'verb', 'recipient', 'notification_type', 'is_read', 'timestamp']
    list_filter = ['notification_type', 'is_read', 'timestamp']
    search_fields = ['actor__username', 'recipient__username', 'verb']
    readonly_fields = ['timestamp']
    list_per_page = 20
    
    def mark_as_read(self, request, queryset):
        updated_count = queryset.update(is_read=True)
        self.message_user(request, f'{updated_count} notifications marked as read.')
    
    def mark_as_unread(self, request, queryset):
        updated_count = queryset.update(is_read=False)
        self.message_user(request, f'{updated_count} notifications marked as unread.')
    
    mark_as_read.short_description = "Mark selected notifications as read"
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    actions = [mark_as_read, mark_as_unread]