from django.contrib import admin
from django.urls import path, include

from apps.home.views import LandingPage

urlpatterns = [
    path('', LandingPage.as_view(), name='home'),

]
