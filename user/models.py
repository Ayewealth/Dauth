# users/models.py
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, null=True, blank=True)

    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class InstructorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pics = models.ImageField(
        default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Course(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255)
    what_you_learn = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    targeted_audience = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="courses")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_hours = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at', 'updated_at']

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
