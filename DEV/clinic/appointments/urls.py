from django.urls import path
from .views import all_appointments_view, update_appointments_view, schedule_appointment

urlpatterns = [
    path('appointments/', all_appointments_view),
    path('appointments/<int:_id>/', update_appointments_view),
    path('marcacao/', schedule_appointment),

]
