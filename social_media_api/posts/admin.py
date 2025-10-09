from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'likes_count', 'comments_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'content_preview']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username']
    readonly_fields = ['created_at']