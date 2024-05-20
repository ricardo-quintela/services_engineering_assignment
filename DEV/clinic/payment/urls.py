from django.urls import path
from .views import payment_option

urlpatterns = [
    path('payment/', payment_option),
]
