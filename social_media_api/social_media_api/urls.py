from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse

def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({
        "status": "healthy",
        "service": "Social Media API",
        "version": "1.0.0"
    })

def index(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Social Media API</title></head>
    <body>
        <h1>Social Media API</h1>
        <p><a href="/api/">Go to API</a></p>
        <p><a href="/admin/">Admin</a></p>
        <p><a href="/health/">Health Check</a></p>
    </body>
    </html>
    """)

def api_root(request):
    return JsonResponse({
        "message": "Social Media API Root",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth/",
            "posts": "/api/posts/",
            "notifications": "/api/notifications/",
            "feed": "/api/posts/feed/",
            "health": "/health/"
        },
        "documentation": "Check README.md for API usage"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/', api_root),
    path('health/', health_check, name='health-check'),
    path('', index),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='post-unlike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)