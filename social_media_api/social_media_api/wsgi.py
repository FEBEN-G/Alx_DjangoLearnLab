"""
WSGI config for social_media_api project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

application = get_wsgi_application()

# Add WhiteNoise for static files (only if installed)
try:
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root="staticfiles")
except ImportError:
    # WhiteNoise not installed, continue without it
    pass