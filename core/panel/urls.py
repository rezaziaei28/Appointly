from django.urls import path
from panel.views import *

app_name = 'panel'

urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='cancel_appointment'),

]