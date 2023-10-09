from django.contrib import admin
from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, BaseADmin, UserCreateView, UserProfileView, UserUpdateView, \
    ChangePasswordView, cargar_departamentos

urlpatterns = [

    path('register/', RegistrationView.as_view(), name='register'),


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('baseadmin/', BaseADmin.as_view(), name='home_admin'),
    path('cargar_departamentos/', cargar_departamentos, name='cargar_departamentos'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('users-profile/<int:pk>/', UserProfileView.as_view(), name='users-profile'),
    path('users-profile/edit/', UserUpdateView, name='users-profile-edit'),
    path('users-profile/change-password/', ChangePasswordView, name='users-profile-change-password'),
]