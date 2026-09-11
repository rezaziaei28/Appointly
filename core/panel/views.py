from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class PanelView(TemplateView):
    template_name = 'panel/panel.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)