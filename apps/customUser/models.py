from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models



class Departamento(models.Model):
    nombre = models.CharField(max_length=200)
    noRad = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Organismo(models.Model):
    nombre = models.CharField(max_length=200)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email debe ser proporcionado.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    SECRETARY = 'secretary'
    CLIENT = 'client'

    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (SECRETARY, 'Secretary'),
        (CLIENT, 'Client'),
    ]

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    MUNICIPIOS_CHOICES = [

        ('arroyo_naranjo', 'Arroyo Naranjo'),
        ('boyeros', 'Boyeros'),
        ('centro_habana', 'Centro Habana'),
        ('cerro', 'Cerro'),
        ('cotorro', 'Cotorro'),
        ('diez_de_octubre', 'Diez de Octubre'),
        ('guanabacoa', 'Guanabacoa'),
        ('habana_del_este', 'Habana del Este'),
        ('habana_vieja', 'Habana Vieja'),
        ('la_lisa', 'La Lisa'),
        ('mantilla', 'Mantilla'),
        ('marianao', 'Marianao'),
        ('plaza', 'Plaza de la Revolución'),
        ('regla', 'Regla'),
        ('san_miguel_del_padron', 'San Miguel del Padrón'),
        ('playa', 'Playa'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=100)
    municipality = models.CharField(max_length=50, choices=MUNICIPIOS_CHOICES)
    ci = models.CharField(max_length=15)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=True, blank=True)

    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    # No se incluye el campo 'phones' aquí

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()


class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='phone_numbers')
    phone_number = models.CharField(max_length=20)