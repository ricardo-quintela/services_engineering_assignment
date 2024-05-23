from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/admin/$", consumers.Consumer.as_asgi()),
]