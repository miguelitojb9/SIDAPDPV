from django.contrib import admin
from django.urls import path

from apps.siapdpv.views import QuejaCreateView, QuejaListView

urlpatterns = [
    path('siapdpv/quejas_list/', QuejaListView.as_view(), name='quejas_list'),
    path('siapdpv/quejas_create/', QuejaCreateView.as_view(), name='quejas_create'),

]