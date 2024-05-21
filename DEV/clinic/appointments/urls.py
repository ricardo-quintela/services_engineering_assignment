from django.urls import path
from .views import all_appointments_view, update_appointments_view, schedule_appointment, all_appointments_view_id

urlpatterns = [
    path('appointments/', all_appointments_view),
    path('appointments_list/', all_appointments_view_id),
    path('appointments/<int:_id>/', update_appointments_view),
    path('scheduling/', schedule_appointment),

]
