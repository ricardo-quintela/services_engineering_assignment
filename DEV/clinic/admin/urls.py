from django.urls import path
from .views import base_app_view, admin_app_view

urlpatterns = [
    path('', base_app_view),
    path('admin/', admin_app_view),
]
