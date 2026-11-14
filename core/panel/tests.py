import os
from django.test import TestCase
from django.urls import reverse
from datetime import date, time
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from booking.models import Doctor, Specialty, Appointment
# Create your tests here.

class PatientPanelTest(TestCase):
      def setUp(self):
            self.user = User.objects.create_user(phone_number="09126666666")
            self.user.profile.first_name = "علی"
            self.user.profile.save()
            self.client.force_login(self.user)

      def test_panel_access_logged_in(self):
            """Test if logged-in user can access panel"""
            response = self.client.get(reverse('panel:panel'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'panel/panel.html')

      def test_panel_access_anonymous(self):
            """Test if anonymous user is redirected to login"""
            self.client.logout()
            response = self.client.get(reverse('panel:panel'))
            self.assertEqual(response.status_code, 302) # Redirect to login


class DoctorPanelTest(TestCase):
      def setUp(self):
            self.specialty = Specialty.objects.create(name="پوست و مو")
            self.user_doctor = User.objects.create_user(phone_number="09127777777")
            self.user_patient = User.objects.create_user(phone_number="09128888888")
            
            # Load a real image from static folder for the doctor
            image_path = os.path.join(settings.BASE_DIR, 'staticfile', 'img', 'photo_2026-08-22_21-32-23.jpg')
            with open(image_path, 'rb') as f:
                  image_content = f.read()
            
            self.doctor = Doctor.objects.create(
                  user=self.user_doctor,
                  first_name="مریم",
                  last_name="کریمی",
                  specialty=self.specialty,
                  image=SimpleUploadedFile(
                  name='test_doctor_image.jpg', 
                  content=image_content, 
                  content_type='image/jpeg'
                  )
            )
            
            self.client.force_login(self.user_doctor)

      def test_doctor_panel_access(self):
            """Test if doctor can access their own panel"""
            response = self.client.get(reverse('panel:doctor_panel'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'panel/doctor_panel.html')

      def test_patient_cannot_access_doctor_panel(self):
            """Test if patient is redirected from doctor panel"""
            self.client.force_login(self.user_patient)
            # Add first name so it doesn't redirect to register
            self.user_patient.profile.first_name = "بیمار"
            self.user_patient.profile.save()
            
            response = self.client.get(reverse('panel:doctor_panel'))
            self.assertRedirects(response, reverse('panel:panel'))