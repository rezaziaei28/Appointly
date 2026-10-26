from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Doctor(models.Model):
    # Link to the user account (if the doctor has a login)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    visit_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0) # Cost of visit
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"

class WorkingHours(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.last_name} - {self.get_day_of_week_display()}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('done', 'Done'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent double booking: one doctor cannot have two appointments at the same date and time
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'], 
                name='unique_appointment_slot'
            )
        ]

    def __str__(self):
        return f"{self.patient.phone_number} with Dr. {self.doctor.last_name} on {self.date} at {self.time}"