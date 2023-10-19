from django.contrib.auth.decorators import login_required
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
        {"nombre": "Departamento de Inversiones", "noRad": "I"},
        {"nombre": "Departamento de Conservación.", "noRad": "C"},
        {"nombre": "Departamento Jurídico", "noRad": "J"},
        {"nombre": "Departamento de Administración de la Vivienda", "noRad": "Admon.V"},
        {"nombre": "Departamento de Control y Fiscalización", "noRad": "CF"},
        {"nombre": "Departamento de Control de Fondo", "noRad": "Sub.CF"},
        {"nombre": "Departamento de Atención Social", "noRad": "Sub.AS"},
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

@login_required()
def obtener_datos_actualizados(request):
    quejas = 0
    quejas_pendientes = 0
    queja_en_tramite = 0
    quejas_atendidas = 0


    if request.GET.get('quejas-filtro').split('| ')[1] == 'Hoy':
        quejas = Queja.objects.filter(fecha_creacion__day=timezone.now().day).count()
        quejas_pendientes = Queja.objects.filter(enTramite=False, procesado=False,
                                                 fecha_creacion__day=timezone.now().day).count()
        queja_en_tramite = Queja.objects.filter(enTramite=True, procesado=False,
                                                fecha_creacion__day=timezone.now().day).count()
        quejas_atendidas = Queja.objects.filter(procesado=True, fecha_creacion__day=timezone.now().day).count()
    elif request.GET.get('quejas-filtro').split('| ')[1] == 'Este Mes':
        quejas = Queja.objects.filter(fecha_creacion__month=timezone.now().month).count()
        quejas_pendientes = Queja.objects.filter(enTramite=False, procesado=False,
                                                 fecha_creacion__month=timezone.now().month,fecha_creacion__year=timezone.now().year).count()
        queja_en_tramite = Queja.objects.filter(enTramite=False, procesado=False,
                                                fecha_creacion__month=timezone.now().month,fecha_creacion__year=timezone.now().year).count()
        quejas_atendidas = Queja.objects.filter(procesado=True, fecha_creacion__month=timezone.now().month,fecha_creacion__year=timezone.now().year).count()
    elif request.GET.get('quejas-filtro').split('| ')[1] == 'Este Año':
        quejas = Queja.objects.filter(fecha_creacion__year=timezone.now().year).count()
        quejas_pendientes = Queja.objects.filter(enTramite=True, procesado=False,
                                                 fecha_creacion__year=timezone.now().year).count()
        queja_en_tramite = Queja.objects.filter(enTramite=True, procesado=False,
                                                fecha_creacion__year=timezone.now().year).count()
        quejas_atendidas = Queja.objects.filter(procesado=True,fecha_creacion__year=timezone.now().year).count()



    denuncia = 0  # Reemplaza esto con tu lógica para obtener el número de denuncias actualizado
    demanda = 0  # Reemplaza esto con tu lógica para obtener el número de demandas actualizado
    clientes = User.objects.filter(role='client').count()  # Reemplaza esto con tu lógica para obtener el número de clientes actualizado

    data = {
        'quejas': quejas,
        'quejas_pendientes': quejas_pendientes,
        'queja_en_tramite': queja_en_tramite,
        'quejas_atendidas': quejas_atendidas,
        'denuncia': denuncia,
        'demanda': demanda,
        'clientes': clientes,
    }
    return JsonResponse(data)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


@csrf_exempt
@login_required()
def datos_departamentos(request):
    # Obtener los datos de los departamentos desde tu fuente de datos
    datos_departamentos = Departamento.objects.annotate(cantidad=Count('quejas')).values('nombre', 'cantidad')

    # Crear una lista de objetos con los datos necesarios para el gráfico
    datos_grafico = []
    for departamento in datos_departamentos:
        datos_grafico.append({
            'value': departamento['cantidad'],
            'name': departamento['nombre']
        })

    # Crear el objeto de configuración del gráfico
    chart_options = {
        'tooltip': {
            'trigger': 'item'
        },
        'legend': {
            'top': '0%',
            'left': 'rigth'
        },
        'series': [{
            'name': 'Access From',
            'type': 'pie',
            'radius': ['40%', '70%'],
            'avoidLabelOverlap': False,
            'label': {
                'show': False,
                'position': 'center',
                'formatter': '{b}: {c}'
            },
            'emphasis': {
                'label': {
                    'show': True,
                    'fontSize': '18',
                    'fontWeight': 'bold'
                }
            },
            'labelLine': {
                'show': False
            },
            'data': datos_grafico
        }]
    }

    # Devolver los datos como una respuesta JSON
    return JsonResponse({
        'chartOptions': chart_options
    })