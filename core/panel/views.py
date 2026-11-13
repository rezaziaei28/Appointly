from django.shortcuts import render ,redirect ,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from booking.models import Specialty

from booking.models import Appointment, WorkingHours
from accounts.models import Profile
# Create your views here.

class PanelView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/panel.html'
    login_url = 'accounts:login' # Redirect to login if not logged in

    def get(self, request, *args, **kwargs):
       # Get profile or create it if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        # If profile is incomplete (no first name), send to register
        if not profile.first_name:
            return redirect('accounts:register')
        
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
        
        context = {
            'profile': profile,
            'appointments': appointments,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class AppointmentDetailView(LoginRequiredMixin, TemplateView):
    def get(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        return render(request, 'panel/appointment_detail.html', {'appointment': appointment})

class CancelAppointmentView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        appointment.delete()
        messages.success(request, "نوبت شما با موفقیت لغو شد.")
        return redirect('panel:panel')

from booking.models import Appointment, Doctor

class DoctorPanel(LoginRequiredMixin, TemplateView):
    template_name = "panel/doctor_panel.html"
    login_url = 'accounts:login'

    def get(self, request, *args, **kwargs):
        # Check if the logged-in user is actually a doctor
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            # If user is not a doctor, redirect to normal patient panel
            messages.error(request, "شما دسترسی به پنل پزشکان ندارید.")
            return redirect('panel:panel')

        # Get appointments for this specific doctor
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')
        
        # Count pending appointments
        pending_count = appointments.filter(status='pending').count()

        # Get working hours for the doctor to show in the form
        working_hours = WorkingHours.objects.filter(doctor=doctor)
        # Create a dictionary to easily access working hours by day in template
        hours_dict = {wh.day_of_week: wh for wh in working_hours}

        context = {
            'doctor': doctor,
            'appointments': appointments,
            'pending_count': pending_count,
            'hours_dict': hours_dict, 
            'specialties_list': Specialty.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return redirect('panel:panel')

        # Handle profile update
        if 'update_profile' in request.POST:
            doctor.first_name = request.POST.get('first_name', doctor.first_name)
            doctor.last_name = request.POST.get('last_name', doctor.last_name)
            specialty_id = request.POST.get('specialty')
            if specialty_id:
                doctor.specialty_id = specialty_id
                
            doctor.bio = request.POST.get('bio', doctor.bio)
            doctor.address = request.POST.get('address', doctor.address)
            
            if request.FILES.get('image'):
                doctor.image = request.FILES.get('image')
                
            doctor.save()
            messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد.")
            return redirect('panel:doctor_panel')

        # Handle working hours update
        if 'update_schedule' in request.POST:
            WorkingHours.objects.filter(doctor=doctor).delete()

            days_mapping = {
                '0': 5, # Saturday
                '1': 6, # Sunday
                '2': 0, # Monday
                '3': 1, # Tuesday
                '4': 2, # Wednesday
                '5': 3, # Thursday
                '6': 4, # Friday
            }

            for i in range(7):
                if f'day_{i}' in request.POST:
                    start_time = request.POST.get(f'start_{i}')
                    end_time = request.POST.get(f'end_{i}')
                    capacity = request.POST.get(f'capacity_{i}', 10)
                    
                    if start_time and end_time:
                        WorkingHours.objects.create(
                            doctor=doctor,
                            day_of_week=days_mapping[str(i)],
                            start_time=start_time,
                            end_time=end_time,
                            capacity=capacity
                        )

            messages.success(request, "برنامه کاری با موفقیت ذخیره شد.")
            return redirect('panel:doctor_panel')

        