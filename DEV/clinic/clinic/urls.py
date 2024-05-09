from django.urls import path, include
from rest_framework import routers

from authentication.views import UserViewSet
from authentication.views import login_view, logout_view
from home.views import home_page_view

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", home_page_view),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("login/", login_view),
    path("logout/", logout_view)
]