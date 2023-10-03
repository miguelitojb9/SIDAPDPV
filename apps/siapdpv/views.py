from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.siapdpv.forms import QuejaForm
from apps.siapdpv.models import Queja, Documento

from django.contrib.auth.mixins import LoginRequiredMixin


class QuejaCreateView(LoginRequiredMixin, CreateView):
    model = Queja
    form_class = QuejaForm
    template_name = 'queja/queja_create.html'  # Plantilla para el formulario
    success_url = reverse_lazy('home')  # URL a la que se redireccionará después de crear la queja

    def form_valid(self, form):
        form.instance.recurrente = self.request.user
        form.instance.municipio = self.request.user.municipality
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

        if user.role == 'client':
            # Mostrar solo las quejas del usuario actual
            return Queja.objects.filter(recurrente=user)
        elif user.role == 'admin':
            # Mostrar todas las quejas del sistema
            return Queja.objects.all()
        elif user.departamentos.first():
            # Mostrar las quejas asociadas al departamento del usuario
            return Queja.objects.filter(departamento=user.departamentos.first())
        else:
            # En caso de otros roles o usuarios sin departamento, no mostrar ninguna queja
            return Queja.objects.none()