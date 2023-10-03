from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, LoginForm, UserForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView

from apps.siapdpv.models import Organismo, Departamento
from .models import User

class BaseADmin(TemplateView):
    template_name = 'useradmin/base_user_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la lista de usuarios
        usuarios = User.objects.all()
        context['usuarios'] = usuarios
        context['usuarios_c'] = usuarios.count()

        # Obtener la cantidad de usuarios en departamentos
        usuarios_en_departamentos = User.objects.exclude(departamentos__isnull=True).count()
        context['usuarios_en_departamentos'] = usuarios_en_departamentos

        departamentos = Departamento.objects.all().count()
        context['cant_departamentos'] = departamentos

        # # Obtener la cantidad de organismos existentes
        # cantidad_organismos = Organismo.objects.count()
        # context['cantidad_organismos'] = cantidad_organismos

        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'useradmin/user_create.html'
    success_url = reverse_lazy('home_admin')

    def form_valid(self, form):
        # Asignar el departamento al usuario
        user = form.save(commit=False)
        departamento = form.cleaned_data['departamento']
        user.save()
        departamento.usuarios.add(user)
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'useradmin/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'role', 'departamento']
    template_name = 'useradmin/user_update.html'
    success_url = reverse_lazy('user-list')


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(str(reverse_lazy('home')))
            else:
                form.add_error(None, 'Email o contraseña incorrectos.')
        return render(request, 'registration/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(str(reverse_lazy('login')))