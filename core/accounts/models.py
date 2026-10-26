from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import random

# Create your models here.

class CustomUserManager(BaseUserManager):
    # Create a regular user with phone number
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_("The Phone Number field must be set"))
        
        user = self.model(phone_number=phone_number, **extra_fields)

        # If password is provided, hash it; otherwise set unusable password (for OTP login)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    # Create a superuser for admin panel
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    # Remove default username field
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    national_id = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.first_name}"


class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    @classmethod
    # Generate a 6-digit random code and save it to database
    def generate_code(cls, phone_number):
        code = str(random.randint(100000, 999999))
        
        # Delete previous unused codes for this number
        cls.objects.filter(phone_number=phone_number, is_used=False).delete()
        
        return cls.objects.create(phone_number=phone_number, code=code)