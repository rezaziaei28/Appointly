from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta

from .models import OTP, User, Profile
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

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        otp_digits = request.POST.getlist('otp') 
        otp_code = "".join(otp_digits)

        if not phone_number or len(otp_code) != 6:
            messages.error(request, "کد وارد شده نامعتبر است")
            return render(request, self.template_name, {'phone_number': phone_number})

        try:
            otp_obj = OTP.objects.get(phone_number=phone_number, code=otp_code, is_used=False)
        except OTP.DoesNotExist:
            messages.error(request, "کد تایید اشتباه است")
            return render(request, self.template_name, {'phone_number': phone_number})

        time_threshold = timezone.now() - timedelta(minutes=2)
        if otp_obj.created_at < time_threshold:
            otp_obj.delete()
            messages.error(request, "کد تایید منقضی شده است")
            return render(request, self.template_name, {'phone_number': phone_number})

        user, created = User.objects.get_or_create(phone_number=phone_number)

        otp_obj.is_used = True
        otp_obj.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # If it's a new user, send them to complete their profile
        if created:
            return redirect('accounts:register') 
        
        return redirect('accounts:register') 

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        national_id = request.POST.get('national_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not first_name or not last_name:
            # check importing first_name and last_name
            messages.error(request, "نام و نام خانوادگی الزامی است")
            return render(request, self.template_name)

        if password != confirm_password:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیستند")
            return render(request, self.template_name)

        # Update user password
        if password:
            request.user.set_password(password)
            request.user.save()

        # Create or update profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.national_id = national_id
        profile.save()

        messages.success(request, "اطلاعات با موفقیت ثبت شد")
        return redirect('panel:panel')

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