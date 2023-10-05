from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
from django.views.generic import TemplateView

from apps.siapdpv.models import Queja
from apps.customUser.models import User


class LandingPage(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard_admin.html'


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
