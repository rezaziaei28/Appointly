from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from booking.models import Appointment
from accounts.models import Profile
# Create your views here.

class PanelView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/panel.html'

    def get(self, request, *args, **kwargs):
       # Get the profile
        profile = get_object_or_404(Profile, user=request.user)

        # Get appointments
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
        
        context = {
            'profile': profile,
            'appointments': appointments,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)