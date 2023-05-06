from django.shortcuts import render, redirect
from django.views.generic import View
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from autentificacion.forms import CustomUserCreationForm, CustomAuthenticationForm, Update_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from publicaciones.models import Categoria, Publicaciones
User = get_user_model()
# Create your views here.

def opciones_login(request):
    return render(request, "autentificacion/index.html")

class VRegistro(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "autentificacion/register.html", {"form":form})
        
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("opciones_login")
        else:
            return render(request, "autentificacion/register.html", {"form":form})

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

@login_required
def perfil(request):
    categorias = Categoria.objects.all()
    user = request.user
    publicaciones_user = Publicaciones.objects.filter(autor = user).order_by("-created")
    return render(request, "autentificacion/perfil.html", {"categorias":categorias, "usuario":user, "publicaciones" : publicaciones_user})

@login_required
def configuracion(request):
    categorias = Categoria.objects.all()

    usuario = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        #formulario
        form = Update_user(request.POST,request.FILES, instance=usuario)
        #si el formato es valido
        if form.is_valid() :
            form.save()
            messages.success(request, 'Tu Perfil ha sido Actualizado Correctamente')
            return redirect("perfil")
    else:
        form = Update_user(instance=usuario)

    return render(request, "autentificacion/configuracion.html", {"categorias":categorias, "form": form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'autentificacion/change_password.html'
    success_message = "Contraseña Actualizada Correctamente"
    success_url = reverse_lazy('perfil')

@login_required
def delete_account(request):
    try:
        usuario = User.objects.get(id=request.user.id)
        usuario.delete()
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect("opciones_login")
    except Exception as e:
        print(e.message)
    finally:
        return redirect("opciones_login")
    

@login_required
def perfil_id(request, id):
    categorias = Categoria.objects.all()
    user = User.objects.get(id=id)
    publicaciones_user = Publicaciones.objects.filter(autor = user).order_by("-created")
    return render(request, "autentificacion/perfil.html", {"categorias":categorias, "usuario":user, "publicaciones" : publicaciones_user})
