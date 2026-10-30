from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from .models import Doctor
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