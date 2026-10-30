from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib import messages

from .models import Doctor, Appointment
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
        # Get the doctor by ID
        doctor = get_object_or_404(Doctor, pk=pk)
        # Pass doctor to template
        return render(request, self.template_name, {'doctor': doctor})

    def post(self, request, pk, *args, **kwargs):
        # Get the doctor by ID or return 404
        doctor = get_object_or_404(Doctor, pk=pk)
        
        # Get the selected date and time from the form
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        # Convert strings to python date and time objects
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        # Create the appointment
        Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            date=date_obj,
            time=time_obj,
            status='pending'
        )

        messages.success(request, "نوبت شما با موفقیت ثبت شد")
        return redirect('panel:panel')