"""
ASGI config for pizza_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

# NEW, adding channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_project.settings')

# application = get_asgi_application()
#NEW channels config instead of above.

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns,
        )
    ),
})
