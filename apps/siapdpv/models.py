from django.db import models
from apps.customUser.models import User, Departamento, Organismo
from django.core.exceptions import ValidationError
from django.utils import timezone


class Tramite(models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    tipo_tramite = models.CharField(max_length=10, choices={
        ('I', 'Queja'),
        ('II', 'Demanda'),
        ('IV', 'Solicitud'),
    })
    aprobado = models.BooleanField(default=False)
    usuario_responsable = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    fecha_respuesta = models.DateField(blank=True, null=True)
    codificacion = models.CharField(max_length=10, blank=True, null=True)

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
    asunto = models.CharField(max_length=200, choices={
        ('101', 'Inmuebles (Casa, apartamento, ciudadelas, etc.)'),
        ('102', 'Ampliación'),
        ('103', 'Permuta entre particulares'),
        ('104', 'Permuta entre particulares y el Estado'),
        ('105', 'Albergue'),
        ('106', 'Inversión y rehabilitación  de vivienda'),
        ('107', 'Materiales de Construcción (Comisión de distribución  expendedores, etc.)'),
        ('108', 'Reparación y Construcciones (Núcleo Familiares)'),
        ('109', 'Reparación y Construcciones colectiva Edificios multifamiliares, ciudadelas, etc.)'),
        ('110', 'Crédito'),
        ('111', 'Incorporación a Micro brigadas, Bajo  Costo o Esfuerzo Propio'),
        ('112', 'Movimiento de Micro brigada'),
        ('113', 'Litigios (Reclamaciones de derechos sobre inmuebles, límite de terreno, uso de área '
                'común entre particulares y el Estado)'),
        ('114', 'Solares'),
        ('115', 'Compra y venta (Ilegalidades)'),
        ('116', 'Legalización de vivienda y solares'),
        ('117', 'Sobre Funcionarios de la Vivienda'),
        ('118', 'Ley  General de la Vivienda (Consultas, críticas, sugerencias)'),
        ('119', 'Comisiones de Asignación de viviendas'),
        ('120', 'Afectaciones del Estado o Particulares'),
        ('121', 'Vivienda vinculadas y medios básicos (No incluye los consultorios MF)'),
        ('122', 'Ocupaciones ilegales (no incluye las construcciones autorizadas)'),
        ('123', 'Inmigración Interna (Decreto ley 217)'),
        ('124', 'Confiscaciones)'),
        ('125', 'Construcciones ilegales (extracciones, demoliciones, etc.))'),
        ('126', 'Arrendamiento  en moneda nacional o libremente convertible)'),
        ('127', 'Licencia para nuevas construcciones'),
        ('128', 'Funcionamiento del Arquitecto de la Comunidad'),
        ('129', 'Sobre trabajadores, dirigentes y funcionarios'),
        ('130', 'Otros asuntos'),
    })
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
