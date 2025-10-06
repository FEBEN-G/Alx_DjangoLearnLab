import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Import original settings
from LibraryProject.settings import *

# Override for testing
ALLOWED_HOSTS = ['*']
DEBUG = True

# Make sure django_extensions is in INSTALLED_APPS
if 'django_extensions' not in INSTALLED_APPS:
    INSTALLED_APPS.append('django_extensions')
