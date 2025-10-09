from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.reverse import reverse

@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow anyone to access
def api_root(request, format=None):
    """
    Social Media API Root Endpoint - Public Access
    """
    base_url = request.build_absolute_uri('/')
    
    response_data = {
        'message': 'Welcome to Social Media API',
        'version': '1.0',
        'authentication_required': 'Most endpoints require JWT authentication',
        'public_endpoints': {
            'register': f'{base_url}api/auth/register/',
            'login': f'{base_url}api/auth/login/',
            'api_root': f'{base_url}api/',
        },
        'authenticated_endpoints': {
            'profile': f'{base_url}api/auth/profile/',
            'users': f'{base_url}api/auth/users/',
            'posts': f'{base_url}api/posts/',
            'feed': f'{base_url}api/feed/',
            'comments': f'{base_url}api/comments/',
        },
        'documentation': 'Check README.md for detailed API documentation',
        'authentication_info': {
            'method': 'JWT Bearer Token',
            'login_to_get_token': f'{base_url}api/auth/login/',
            'header_format': 'Authorization: Bearer <your_token>'
        }
    }
    
    # If user is authenticated, show personalized info
    if request.user.is_authenticated:
        response_data.update({
            'authenticated_user': {
                'username': request.user.username,
                'id': request.user.id,
            },
            'message': f'Welcome back, {request.user.username}!'
        })
    
    return Response(response_data)