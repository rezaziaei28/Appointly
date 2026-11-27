from django.contrib import admin

from .models import Doctor, WorkingHours, Appointment, Specialty, Review
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty', 'user')
    fields = ('user', 'first_name', 'last_name', 'specialty', 'bio', 'address', 'phone_number', 'image', 'visit_fee', 'is_active')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'is_displayed', 'created_at')
    list_filter = ('is_displayed', 'rating')
    search_fields = ('doctor__last_name', 'patient__phone_number', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_displayed=True)
    approve_reviews.short_description = "Approve selected reviews"

admin.site.register(WorkingHours)
admin.site.register(Specialty)
admin.site.register(Appointment)