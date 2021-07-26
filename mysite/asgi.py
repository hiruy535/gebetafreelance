import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
ASGI_APPLICATION = "routing.application"
application = get_default_application()
