from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import RegistrationForm, LoginForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, DetailView

from .models import User,Departamento,Organismo


class UserProfileView(DetailView):
    model = User
    template_name = 'useradmin/users-profile.html'
    context_object_name = 'user'

@login_required
def cargar_departamentos(request):
    objs = Departamento.objects.all()
    data = [{'id': obj.id, 'name': obj.nombre} for obj in objs]
    return JsonResponse(data, safe=False)

class BaseADmin(TemplateView):
    template_name = 'useradmin/base_user_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la lista de usuarios
        usuarios = User.objects.all()

        if self.request.user.departamento is not None:
            pass
            # context['usuarios'] = usuarios.filter(departamento__in=self.request.user.departamento.all())
            # context['usuarios_c'] = usuarios.filter(departamento__in=self.request.user.departamento.all()).count()
        else:
            context['usuarios'] = usuarios
            context['usuarios_c'] = usuarios.count()

        # Obtener la cantidad de usuarios en departamentos
        usuarios_en_departamentos = User.objects.exclude(departamento__isnull=True).count()
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



class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'useradmin/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')


@login_required
@csrf_exempt
def UserUpdateView(request):
    if request.method == 'POST':
        user = request.user
        user.nombre = request.POST['nombre']
        user.apellidos = request.POST['apellidos']
        user.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Método de solicitud no válido.'})


@login_required
@csrf_exempt
def ChangePasswordView(request):
    if request.method == 'POST':
        data = {
            'old_password': request.POST['old_password'],
            'new_password1': request.POST['new_password1'],
            'new_password2': request.POST['new_password2'],


        }
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualizar la sesión del usuario con la nueva contraseña
            return JsonResponse({'success': True})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Método de solicitud no válido.'})


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


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(str(reverse_lazy('login')))
