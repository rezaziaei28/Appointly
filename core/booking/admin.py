from django.contrib import admin

from .models import Doctor, WorkingHours, Appointment
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty', 'user')
    fields = ('user', 'first_name', 'last_name', 'specialty', 'bio', 'address', 'phone_number', 'image', 'visit_fee', 'is_active')

admin.site.register(WorkingHours)
admin.site.register(Appointment)