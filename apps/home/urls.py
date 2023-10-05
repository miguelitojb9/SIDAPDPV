from django.contrib import admin
from django.urls import path, include

from apps.home.views import LandingPage, obtener_datos_actualizados

urlpatterns = [
    path('', LandingPage.as_view(), name='home'),
    path('obtener-datos-actualizados/', obtener_datos_actualizados, name='obtener_datos_actualizados'),

]
