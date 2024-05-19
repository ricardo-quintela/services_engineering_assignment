from django.urls import path
from .views import users_view, all_users_view, login_view, register_view, upload_image_view, facial_recognition_view

urlpatterns = [
    path('users/', all_users_view),
    path('users/<int:user_id>/', users_view),
    path('login/', login_view),
    path('register/', register_view),
    path('image/', upload_image_view),
    path('recognition/', facial_recognition_view),
]
