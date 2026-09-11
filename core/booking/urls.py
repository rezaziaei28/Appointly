from django.urls import path
from booking.views import *


app_name = 'booking'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('doctor/',DoctorDetailView.as_view(),name='doctor_detail'),
    path('booking/', BookAppointmentView.as_view(), name='book_appointment'),
]