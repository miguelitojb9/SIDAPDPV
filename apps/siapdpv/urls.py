from django.contrib import admin
from django.urls import path

from apps.siapdpv.views import QuejaCreateView, QuejaListView, load_queja_info, asignar_departamento, CrearTramiteView, \
    ListarTramitesDepartamentoView, load_tramite_info, CrearRespuestaTramiteView

urlpatterns = [
    path('siapdpv/quejas_list/', QuejaListView.as_view(), name='quejas_list'),
    path('siapdpv/quejas_create/', QuejaCreateView.as_view(), name='quejas_create'),
    path('siapdpv/load_queja_info/', load_queja_info, name='load_queja_info'),
    path('siapdpv/asignar_departamento/', asignar_departamento, name='asignar_departamento'),



    path('siapdpv/queja/<int:queja_id>/crear_tramite/', CrearTramiteView.as_view(), name='crear_tramite'),
    path('siapdpv/lista_tramites/', ListarTramitesDepartamentoView.as_view(), name='lista_tramites'),
    path('siapdpv/load_tramite_info/', load_tramite_info, name='load_tramite_info'),
    path('siapdpv/resp_tramite/', CrearRespuestaTramiteView.as_view(), name='resp_tramite'),


]