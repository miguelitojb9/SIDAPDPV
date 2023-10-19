from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError


class Departamento(models.Model):
    nombre = models.CharField(max_length=200)
    noRad = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Organismo(models.Model):
    nombre = models.CharField(max_length=200)
    noRad = models.CharField(max_length=200, null=True, blank=True)


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
    CLIENT = 'client'

    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
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
        ('marianao', 'Marianao'),
        ('plaza', 'Plaza de la Revolución'),
        ('regla', 'Regla'),
        ('san_miguel_del_padron', 'San Miguel del Padrón'),
        ('playa', 'Playa'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    direccion = models.CharField(max_length=100)
    municipio = models.CharField(max_length=50, choices=MUNICIPIOS_CHOICES)
    ci = models.CharField(max_length=15)

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE, null=True, blank=True)

    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    # No se incluye el campo 'phones' aquí

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.departamento and self.organismo:
            raise ValidationError("A user cannot be associated with both a department and an organization.")
        super().save(*args, **kwargs)


class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='phone_numbers')
    phone_number = models.CharField(max_length=20)