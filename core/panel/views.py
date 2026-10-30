from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from booking.models import Appointment
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