from django.contrib import admin
from django.urls import path

from apps.siapdpv.views import QuejaCreateView, QuejaListView, load_queja_info, asignar_departamento

urlpatterns = [
    path('siapdpv/quejas_list/', QuejaListView.as_view(), name='quejas_list'),
    path('siapdpv/quejas_create/', QuejaCreateView.as_view(), name='quejas_create'),
    path('siapdpv/load_queja_info/', load_queja_info, name='load_queja_info'),
    path('siapdpv/asignar_departamento/', asignar_departamento, name='asignar_departamento'),

]