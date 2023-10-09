from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.defaulttags import csrf_token
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.siapdpv.forms import QuejaForm
from apps.siapdpv.models import Queja, Documento

from django.contrib.auth.mixins import LoginRequiredMixin

from ..customUser.models import Departamento


class QuejaCreateView(LoginRequiredMixin, CreateView):
    model = Queja
    form_class = QuejaForm
    template_name = 'queja/queja_create.html'  # Plantilla para el formulario
    success_url = reverse_lazy('quejas_list')  # URL a la que se redireccionará después de crear la queja

    def form_valid(self, form):
        form.instance.recurrente = self.request.user
        form.instance.municipio = self.request.user.get_municipality_display()
        response = super().form_valid(form)


        archivos = self.request.FILES.getlist('archivos')

        for archivo in archivos:
            Documento.objects.create(queja=self.object, archivo=archivo)

        # Preparar la respuesta JSON indicando el éxito del envío del formulario

        response_data = {'success': True}

        # Enviar la respuesta JSON al cliente
        return JsonResponse(response_data)


class QuejaListView(LoginRequiredMixin, ListView):
    model = Queja
    template_name = 'queja/queja_list.html'  # Plantilla para mostrar la lista de quejas
    context_object_name = 'quejas'  # Nombre del objeto de contexto para la lista de quejas

    def get_queryset(self):
        user = self.request.user

        if user.departamento:
            # Mostrar las quejas asociadas al departamento del usuario
            return Queja.objects.filter(departamento_asignado=user.departamento)
        elif user.role == 'client':
            # Mostrar solo las quejas del usuario actual
            return Queja.objects.filter(recurrente=user)
        elif user.role == 'admin':
            # Mostrar todas las quejas del sistema
            return Queja.objects.filter(departamento_asignado=None)
        else:
            # En caso de otros roles o usuarios sin departamento, no mostrar ninguna queja
            return Queja.objects.none()


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Queja


def load_queja_info(request):
    queja_id = request.GET.get('queja_id')
    queja = get_object_or_404(Queja, id=queja_id)
    # Convertir el objeto Queja a un diccionario


    queja_dict = {
        'id': queja.id,
        'fecha': queja.fecha_creacion.strftime('%Y-%m-%d'),
        'titulo': queja.asunto,
        'descripcion': queja.descripcion,


    }
    try:
        documento = Documento.objects.get(queja_id=queja.id)
        queja_dict['documento'] = documento.archivo.url
    except Documento.DoesNotExist:
        queja_dict['documento'] = None


    # Renderiza un template que contenga la información de la queja en el modal
    return JsonResponse({'data': queja_dict})

import json
from django.http import JsonResponse


def assign_department(request):
    if request.method == 'POST':
        queja_id = request.POST.get('queja_id')
        departamento_id = request.POST.get('departamento_id')
        queja = get_object_or_404(Queja, id=queja_id)
        departamento = get_object_or_404(Departamento, id=departamento_id)
        queja.departamento = departamento
        queja.save()

        # Convertir el objeto Queja a un diccionario
        queja_dict = {
            'id': queja.id,
            'titulo': queja.titulo,
            'descripcion': queja.descripcion,
            'departamento': {
                'id': departamento.id,
                'nombre': departamento.nombre
            }
        }

        return JsonResponse({'success': True, 'queja': queja_dict})
    else:
        return JsonResponse({'success': False})



@login_required()
def asignar_departamento(request):
    if request.method == 'POST':
        try:
            queja = get_object_or_404(Queja, id=request.POST.get('queja_id'))
            departamento_id = request.POST.get('depto_id')
            departamento = get_object_or_404(Departamento, id=departamento_id)
            queja.departamento_asignado = departamento
            queja.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})


    return JsonResponse({'success': False})