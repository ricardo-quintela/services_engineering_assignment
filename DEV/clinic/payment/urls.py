from django.urls import path
from .views import payment_option

urlpatterns = [
    path('payment/<int:_id>/<int:option>/<int:telemovel>/', payment_option),
]
