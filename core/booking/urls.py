from django.urls import path
from booking.views import *


app_name = 'booking'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('doctor/<int:pk>/',DoctorDetailView.as_view(),name='doctor_detail'),
    path('booking/<int:pk>/', BookAppointmentView.as_view(), name='book_appointment'),
    path('booking/<int:pk>/confirm/', ConfirmAppointmentView.as_view(), name='confirm_appointment'),
]