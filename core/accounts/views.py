from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import OTP
# Create your views here.


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get('phone')
        
        # Basic validation for phone number length
        if not phone_number or len(phone_number) != 11:
            messages.error(request, "Please enter a valid 11-digit phone number.")
            return render(request, self.template_name)

        # Generate and save OTP
        otp = OTP.generate_code(phone_number)
        
        return render(request, 'accounts/verify.html', {'phone_number': phone_number, "otp": otp.code})

class PasswordView(TemplateView):
    template_name = 'accounts/password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class VerifyView(TemplateView):
    template_name = 'accounts/verify.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ForgotView(TemplateView):
    template_name = 'accounts/forgot.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ResetView(TemplateView):
    template_name = 'accounts/reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)