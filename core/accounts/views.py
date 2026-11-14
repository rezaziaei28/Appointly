from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import OTP, User, Profile
from booking.models import Doctor, Specialty
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
        
        # If user exists, go directly to panel
        return redirect('panel:panel')

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        national_id = request.POST.get('national_id')
        
        if not first_name or not last_name:
            # check importing first_name and last_name
            messages.error(request, "نام و نام خانوادگی الزامی است")
            return render(request, self.template_name)

        # Create or update profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.national_id = national_id
        profile.save()

        messages.success(request, "اطلاعات با موفقیت ثبت شد")
        return redirect('panel:panel')

class LogoutView(TemplateView):
    '''log out user'''
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')

class RoleSelectionView(TemplateView):
    template_name = 'accounts/role_selection.html'

class DoctorLoginView(TemplateView):
    template_name = 'accounts/doctor_login.html'

    def post(self, request):
        phone_number = request.POST.get('phone')

        if not phone_number or len(phone_number) != 11:
            messages.error(request, "Please enter a valid 11-digit phone number.")
            return render(request, self.template_name)

        # generate and save otp
        otp = OTP.generate_code(phone_number)

        return render(request, 'accounts/doctor_verify.html', {
            'phone_number': phone_number,
            'otp': otp.code,
        })

class DoctorVerifyView(TemplateView):
    template_name = 'accounts/doctor_verify.html'

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        otp_digits = request.POST.getlist('otp')
        otp_code = "".join(otp_digits)

        if not phone_number or len(otp_code) != 6:
            messages.error(request, "Invalid verification code.")
            return render(request, self.template_name, {'phone_number': phone_number})

        try:
            otp_obj = OTP.objects.get(phone_number=phone_number, code=otp_code, is_used=False)
        except OTP.DoesNotExist:
            messages.error(request, "Incorrect verification code.")
            return render(request, self.template_name, {'phone_number': phone_number})

        time_threshold = timezone.now() - timedelta(minutes=2)
        if otp_obj.created_at < time_threshold:
            otp_obj.delete()
            messages.error(request, "Verification code has expired.")
            return render(request, self.template_name, {'phone_number': phone_number})

        # get or create user
        doctor_user, created = User.objects.get_or_create(phone_number=phone_number)

        otp_obj.is_used = True
        otp_obj.save()

        login(request, doctor_user, backend='django.contrib.auth.backends.ModelBackend')

        # if doctor profile already exists, go to dashboard
        if hasattr(doctor_user, 'doctor'):
            return redirect('panel:doctor_panel')

        # otherwise complete doctor profile first
        return redirect('accounts:doctor_register')

class DoctorRegisterView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/doctor_register.html'
    login_url = 'accounts:doctor_login'

    def get(self, request, *args, **kwargs):
        # already a doctor? go to dashboard
        if hasattr(request.user, 'doctor'):
            return redirect('panel:doctor_panel')
        specialties = Specialty.objects.filter(is_active=True)
        return render(request, self.template_name, {'specialties': specialties})

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialty_id = request.POST.get('specialty')
        address = request.POST.get('address')
        visit_fee = request.POST.get('visit_fee', 0)

        if not first_name or not last_name:
            messages.error(request, "First name and last name are required.")
            return render(request, self.template_name, {'specialties': Specialty.objects.filter(is_active=True)})

        # create doctor profile
        Doctor.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            specialty_id=specialty_id or None,
            address=address or '',
            visit_fee=visit_fee or 0,
            is_active=True,
        )

        messages.success(request, "Doctor profile completed successfully.")
        return redirect('panel:doctor_panel')