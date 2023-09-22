from django.db import models
from apps.customUser.models import User


class Queja(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey('Departamento', on_delete=models.PROTECT, related_name='quejas', null=True, blank=True)
    organismo_asignado = models.ForeignKey('Organismo', on_delete=models.PROTECT, related_name='solicitudes', null=True, blank=True)


class Demanda(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey('Departamento', on_delete=models.PROTECT, related_name='demandas', null=True, blank=True)


class Solicitud(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey('Departamento', on_delete=models.PROTECT, related_name='solicitudes', null=True, blank=True)


class Nota(models.Model):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, null=True, blank=True)
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, null=True, blank=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.TextField()


class Documento(models.Model):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, null=True, blank=True)
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, null=True, blank=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=True, blank=True)
    archivo = models.FileField(upload_to='documentos/')


class Departamento(models.Model):
    nombre = models.CharField(max_length=200)
    usuarios = models.ManyToManyField(User, related_name='departamentos', null=True, blank=True)


class Tramite(models.Model):
    TIPOS_TRAMITE = (
        ('queja', 'Queja'),
        ('demanda', 'Demanda'),
        ('solicitud', 'Solicitud'),
    )
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    tipo_tramite = models.CharField(max_length=10, choices=TIPOS_TRAMITE)
    aprobado = models.BooleanField(default=False)
    usuario_responsable = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)


class Organismo(models.Model):
    nombre = models.CharField(max_length=200)
    usuarios = models.ManyToManyField(User, related_name='organismos', blank=True, null=True)