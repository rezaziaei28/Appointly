from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('password/', PasswordView.as_view(), name='password'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('reset/', ResetView.as_view(), name='reset'),
]