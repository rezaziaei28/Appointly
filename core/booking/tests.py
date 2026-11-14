from django.test import TestCase
from datetime import date, time

from accounts.models import User
from .models import Doctor, Specialty, WorkingHours, Appointment
# Create your tests here.

class DoctorModelTest(TestCase):
      def setUp(self):
            # Create a specialty
            self.specialty = Specialty.objects.create(name="قلب و عروق")
        
            # Create a user for the doctor
            self.user = User.objects.create_user(phone_number="09120000000")
        
            # Create a doctor
            self.doctor = Doctor.objects.create(
                  user=self.user,
                  first_name="محمد رضا",
                  last_name="ضیایی",
                  specialty=self.specialty,
                  address="نیشابور مرکز شهر",
                  phone_number="02112345678"
            )

      def test_doctor_creation(self):
            """Test if the doctor is created correctly"""
            self.assertEqual(self.doctor.first_name,"محمد رضا")
            self.assertEqual(self.doctor.last_name, "ضیایی")
            self.assertEqual(self.doctor.specialty.name, "قلب و عروق")
            self.assertEqual(str(self.doctor), "Dr. محمد رضا ضیایی - قلب و عروق")

class AppointmentModelTest(TestCase):
      def setUp(self):
            self.specialty = Specialty.objects.create(name="دندانپزشکی")
            self.user_doctor = User.objects.create_user(phone_number="09120000001")
            self.user_patient = User.objects.create_user(phone_number="09120000002")
        
            self.doctor = Doctor.objects.create(
                  user=self.user_doctor,
                  first_name="رضا",
                  last_name="رضایی",
                  specialty=self.specialty
            )
        
            self.appointment = Appointment.objects.create(
                  doctor=self.doctor,
                  patient=self.user_patient,
                  date=date(2026, 12, 1),
                  time=time(10, 30),
                  status='pending'
            )

      def test_appointment_creation(self):
            """Test if the appointment is created correctly"""
            self.assertEqual(self.appointment.doctor, self.doctor)
            self.assertEqual(self.appointment.patient, self.user_patient)
            self.assertEqual(self.appointment.status, 'pending')
            self.assertEqual(self.appointment.date, date(2026, 12, 1))