from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
from django.views.generic import TemplateView

from apps.siapdpv.models import Queja
from apps.customUser.models import User, Departamento

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def adicionar_departamentos():
    departamentos_nuevos = [
        {"nombre": "Dirección", "noRad": "D"},
        {"nombre": "Subdirección General", "noRad": "Sub.G"},
        {"nombre": "Departamento de Cuadro", "noRad": "C"},
        {"nombre": "Subdirección Técnica", "noRad": "Sub.T"},
        {"nombre": "Departamento de Inversiones", "noRad": "I"},
        {"nombre": "Departamento de Conservación.", "noRad": "C"},
        {"nombre": "Subdirección Legal.", "noRad": "Sub.L"},
        {"nombre": "Departamento Jurídico", "noRad": "J"},
        {"nombre": "Departamento de Trámite ", "noRad": "T"},
        {"nombre": "Subdirección de Administración de la Vivienda", "noRad": "Admon.V"},
        {"nombre": "Subdirección de Control y Fiscalización", "noRad": "CF"},
        {"nombre": "Subdirección de Control de Fondo", "noRad": "Sub.CF"},
        {"nombre": "Subdirección de Atención Social", "noRad": "Sub.AS"},
    ]

    for departamento_data in departamentos_nuevos:
        nombre = departamento_data["nombre"]
        noRad = departamento_data["noRad"]

        # Verificar si el departamento ya existe en la base de datos
        if not Departamento.objects.filter(nombre=nombre, noRad=noRad).exists():
            departamento = Departamento(nombre=nombre, noRad=noRad)
            departamento.save()

class LandingPage(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard_admin.html'

    def dispatch(self, request, *args, **kwargs):
        adicionar_departamentos()
        return super().dispatch(request, *args, **kwargs)


def obtener_datos_actualizados(request):
    quejas = 0

    if request.GET.get('quejas-filtro').split('| ')[1] == 'Today':
        quejas = Queja.objects.filter(departamento_asignado=None, fecha_creacion__day=timezone.now().day).count()
    elif request.GET.get('quejas-filtro').split('| ')[1] == 'This Month':
        quejas = Queja.objects.filter(departamento_asignado=None, fecha_creacion__month=timezone.now().month).count()
    elif request.GET.get('quejas-filtro').split('| ')[1] == 'This Year':
        quejas = Queja.objects.filter(departamento_asignado=None, fecha_creacion__year=timezone.now().year).count()


    denuncia = 0  # Reemplaza esto con tu lógica para obtener el número de denuncias actualizado
    demanda = 0  # Reemplaza esto con tu lógica para obtener el número de demandas actualizado
    clientes = User.objects.filter(role='client').count()  # Reemplaza esto con tu lógica para obtener el número de clientes actualizado

    data = {
        'quejas': quejas,
        'denuncia': denuncia,
        'demanda': demanda,
        'clientes': clientes,
    }
    return JsonResponse(data)
