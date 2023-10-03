from django.contrib import admin
from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, BaseADmin, UserCreateView

urlpatterns = [

    path('register/', RegistrationView.as_view(), name='register'),


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('baseadmin/', BaseADmin.as_view(), name='home_admin'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
]