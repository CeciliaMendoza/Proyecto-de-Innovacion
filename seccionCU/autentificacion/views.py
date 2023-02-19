from django.shortcuts import render, redirect
from django.views.generic import View

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from autentificacion.forms import CustomUserCreationForm, CustomAuthenticationForm
# Create your views here.

def opciones_login(request):
    return render(request, "autentificacion/index.html")

class VRegistro(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "Autentificacion/register.html", {"form":form})
        
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("home")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "Autentificacion/register.html", {"form":form})

def login_user(request):
    if request.method=="POST":
        form = CustomAuthenticationForm(request, data= request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username = nombre, password = contra)
            if usuario is not None:
                login(request, usuario)
                return redirect("home")
            else:
                messages.error(request, "Usuario no valido")
        else:
            messages.error(request, "Informacion incorrecta")

    form = CustomAuthenticationForm()
    return render(request, "autentificacion/login.html", {"form":form})

def logout_user(request):
    logout(request)
    return redirect("opciones_login")
