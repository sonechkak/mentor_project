import os
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

# WSGI application
wsgi_application = get_wsgi_application()

# ASGI application
asgi_application = get_asgi_application()

# Default application
application = wsgi_application