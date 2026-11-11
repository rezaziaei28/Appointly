from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('register/', RegisterView.as_view(), name='register'),
]