from django.db import models
from apps.customUser.models import User, Departamento, Organismo
from django.utils import timezone


class Queja(models.Model):
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
        ('playa', 'Playa'),
        ('plaza', 'Plaza de la Revolución'),
        ('regla', 'Regla'),
        ('san_miguel_del_padron', 'San Miguel del Padrón'),
    ]
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100, choices=MUNICIPIOS_CHOICES)
    descripcion = models.TextField(max_length=100,null=True,blank=True)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='quejas',
                                              null=True, blank=True)
    organismo_asignado = models.ForeignKey(Organismo, on_delete=models.PROTECT, related_name='solicitudes',
                                           null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def get_municipio(self):
        return self.get_municipio_display()


class Demanda(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='demandas', null=True, blank=True)


class Solicitud(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='solicitudes', null=True, blank=True)


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

