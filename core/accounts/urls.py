from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('welcome/', RoleSelectionView.as_view(), name='role_selection'),
    path('doctor-login/', DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor-verify/', DoctorVerifyView.as_view(), name='doctor_verify'),
]