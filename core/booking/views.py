from django.shortcuts import render, get_object_or_404 , redirect
from django.views.generic import TemplateView
from datetime import datetime, timedelta, time
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Doctor, Appointment, WorkingHours
# Create your views here.


class HomeView(TemplateView):
    template_name = 'booking/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DoctorDetailView(TemplateView):
    template_name = 'booking/doctor.html'

    def get(self, request, pk, *args, **kwargs):
        # Get the doctor by ID or return 404
        doctor = get_object_or_404(Doctor, pk=pk)
        context = {"doctor": doctor} 
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        return render(request, self.template_name)



class BookAppointmentView(TemplateView):
    template_name = 'booking/booking.html'

    def get(self, request, pk, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=pk)
        today = datetime.now().date()
        available_dates = []

        # Get available dates for the next 30 days
        for i in range(30):
            current_date = today + timedelta(days=i)
            day_of_week = current_date.weekday()
            
            if WorkingHours.objects.filter(doctor=doctor, day_of_week=day_of_week).exists():
                available_dates.append(current_date)

        return render(request, self.template_name, {
            'doctor': doctor, 
            'dates': available_dates,
            'step': 'date'
        })


    def post(self, request, pk, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=pk)
        selected_date_str = request.POST.get('date')
        
        if not selected_date_str:
            return redirect('booking:book_appointment', pk=pk)

        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        day_of_week = selected_date.weekday()
        
        working_hours = WorkingHours.objects.filter(doctor=doctor, day_of_week=day_of_week)
        
        available_times = []
        booked_times = []

        # Generate time slots based on working hours
        for wh in working_hours:
            start_dt = datetime.combine(selected_date, wh.start_time)
            end_dt = datetime.combine(selected_date, wh.end_time)
            
            while start_dt < end_dt:
                time_str = start_dt.strftime('%H:%M')
                is_booked = Appointment.objects.filter(
                    doctor=doctor, 
                    date=selected_date, 
                    time=start_dt.time()
                ).exists()
                
                if is_booked:
                    booked_times.append(time_str)
                else:
                    available_times.append(time_str)
                    
                start_dt += timedelta(minutes=30)

        # Regenerate dates for the sidebar
        today = datetime.now().date()
        available_dates = []
        for i in range(30):
            current_date = today + timedelta(days=i)
            if WorkingHours.objects.filter(doctor=doctor, day_of_week=current_date.weekday()).exists():
                available_dates.append(current_date)

        return render(request, self.template_name, {
            'doctor': doctor,
            'dates': available_dates,
            'times': available_times,
            'booked_times': booked_times,
            'selected_date': selected_date_str,
            'step': 'time'
        })


class ConfirmAppointmentView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/booking.html'
    login_url = 'accounts:login' # Redirect to login if not logged in

    def post(self, request, pk, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=pk)
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        # Check if slot is already booked
        if Appointment.objects.filter(doctor=doctor, date=date_obj, time=time_obj).exists():
            messages.error(request, "This time slot is already booked.")
            return redirect('booking:book_appointment', pk=pk)

        Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            date=date_obj,
            time=time_obj,
            status='pending'
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('panel:panel')

