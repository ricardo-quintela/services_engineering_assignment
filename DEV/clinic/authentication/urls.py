from django.urls import path
from .views import users_view, all_users_view, login_view, teste

urlpatterns = [
    path('users/', all_users_view),
    path('users/<int:user_id>/', users_view),
    path('login/', login_view),
    path('marcacao/', teste),
]
