from django.db import models
from apps.customUser.models import User, Departamento, Organismo
from django.core.exceptions import ValidationError
from django.utils import timezone


class Tramite(models.Model):
    TIPOS_TRAMITE = (
        ('queja', 'Queja'),
        ('demanda', 'Demanda'),
        ('solicitud', 'Solicitud'),
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    tipo_tramite = models.CharField(max_length=10, choices=TIPOS_TRAMITE)
    aprobado = models.BooleanField(default=False)
    usuario_responsable = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    fecha_respuesta = models.DateField(blank=True, null=True)

    # Campos para la respuesta al trámite
    respuesta = models.TextField(blank=True)
    tiene_respuesta = models.BooleanField(default=False)
    adjunto = models.FileField(upload_to='adjuntos/', blank=True, null=True)
    conclusion_queja = models.CharField(max_length=3, choices=(
        ('CR', 'Con Razón'),
        ('CRP', 'Con Razón en Parte'),
        ('SR', 'Sin Razón'),
    ), blank=True, null=True)
    NIVEL_SOLUCION_CHOICES = (
        ('S', 'Solucionado'),
        ('SP', 'Solucionado en Parte'),
        ('SS', 'Sin Solución'),
        ('PS', 'Pendiente a Solución'),
    )

    # Otros campos existentes en el modelo Queja

    nivel_solucion = models.CharField(max_length=2, choices=NIVEL_SOLUCION_CHOICES, blank=True, null=True)

    def clean(self):
        if self.tipo_tramite == 'queja':
            existing_demanda_tramites = Tramite.objects.filter(
                tipo_tramite='queja',
                departamento_asignado=self.departamento_asignado
            )
            if existing_demanda_tramites.exists():
                raise ValidationError('Ya existe un trámite de demanda para este departamento.')

    def save(self, *args, **kwargs):
        if self.aprobado and not self.fecha_respuesta:
            self.fecha_respuesta = timezone.now().date() + timezone.timedelta(days=60)
        super().save(*args, **kwargs)


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
    noRadicacion = models.CharField(max_length=100, null=True, blank=True)
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100, choices=MUNICIPIOS_CHOICES)
    descripcion = models.TextField(max_length=100, null=True, blank=True)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    tramite = models.ForeignKey(Tramite, on_delete=models.PROTECT, null=True, blank=True)
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
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='demandas',
                                              null=True, blank=True)


class Solicitud(models.Model):
    recurrente = models.ForeignKey(User, on_delete=models.PROTECT)
    asunto = models.CharField(max_length=200)
    municipio = models.CharField(max_length=100)
    procesado = models.BooleanField(default=False)
    enTramite = models.BooleanField(default=False)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='solicitudes',
                                              null=True, blank=True)


class Documento(models.Model):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, null=True, blank=True)
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, null=True, blank=True)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=True, blank=True)
    archivo = models.FileField(upload_to='documentos/')
