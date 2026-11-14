from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import User, Profile, OTP
# Create your tests here.

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09121111111",
            password="testpassword123"
        )

    def test_create_user(self):
        """Test if user is created with the correct phone number"""
        self.assertEqual(self.user.phone_number, "09121111111")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_create_superuser(self):
        """Test if superuser is created correctly"""
        admin = User.objects.create_superuser(
            phone_number="09122222222",
            password="adminpassword"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_profile_creation(self):
        """Test if profile is automatically created for user"""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)


class OTPModelTest(TestCase):
    def test_generate_code(self):
        """Test if OTP code is generated and saved"""
        otp = OTP.generate_code("09123333333")
        self.assertEqual(len(otp.code), 6)
        self.assertEqual(otp.phone_number, "09123333333")
        self.assertFalse(otp.is_used)

    def test_otp_expiry(self):
        """Test if old OTP codes are deleted when a new one is generated"""
        otp1 = OTP.generate_code("09124444444")
        otp2 = OTP.generate_code("09124444444")
        self.assertEqual(OTP.objects.filter(phone_number="09124444444").count(), 1)


class LoginViewTest(TestCase):
    def test_login_get(self):
        """Test if login page loads correctly"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_post_invalid_phone(self):
        """Test if short phone number returns error"""
        response = self.client.post(reverse('accounts:login'), {'phone': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a valid 11-digit phone number.")


class RegisterViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number="09125555555")
        self.client.force_login(self.user)

    def test_register_get(self):
        """Test if register page loads correctly"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_post_valid_data(self):
        """Test if profile is updated with name and national id"""
        response = self.client.post(reverse('accounts:register'), {
            'first_name': 'علی',
            'last_name': 'محمدی',
            'national_id': '0012345678'
        })
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.first_name, 'علی')
        self.assertEqual(self.user.profile.last_name, 'محمدی')
        self.assertRedirects(response, reverse('panel:panel'))