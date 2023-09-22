from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy

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