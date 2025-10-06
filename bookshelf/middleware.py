"""
Custom middleware for additional security headers and HTTPS enforcement.
"""

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        
        # Content Security Policy (Basic)
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
        )
        response['Content-Security-Policy'] = csp_policy
        
        # Strict Transport Security (if using HTTPS)
        if getattr(settings, 'SECURE_SSL_REDIRECT', False):
            response['Strict-Transport-Security'] = f'max-age={settings.SECURE_HSTS_SECONDS}; includeSubDomains; preload'
        
        return response

class HTTPSRedirectMiddleware:
    """
    Middleware to enforce HTTPS redirects in production.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we should redirect to HTTPS
        if (getattr(settings, 'SECURE_SSL_REDIRECT', False) and 
            not request.is_secure()):
            # Create HTTPS URL
            url = request.build_absolute_uri(request.get_full_path())
            https_url = url.replace('http://', 'https://')
            return HttpResponsePermanentRedirect(https_url)
        
        return self.get_response(request)