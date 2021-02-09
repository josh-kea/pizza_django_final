from django.urls import re_path

from . import consumers  # Importing consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/order_status/$', consumers.OrderStatusConsumer.as_asgi()),
]