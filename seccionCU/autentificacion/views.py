from django.shortcuts import render, redirect
from django.views.generic import View
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from autentificacion.forms import CustomUserCreationForm, CustomAuthenticationForm, Update_user, Crear_publicacion

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
        return render(request, "Autentificacion/register.html", {"form":form})
        
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("opciones_login")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
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


def perfil(request):
    categorias = Categoria.objects.all()
    user = request.user
    print(request.user.id)
    publicaciones_user = Publicaciones.objects.filter(autor = user)
    return render(request, "autentificacion/perfil.html", {"categorias":categorias, "usuario":user, "publicaciones" : publicaciones_user})

def configuracion(request):
    categorias = Categoria.objects.all()

    usuario = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        #imagen antigua
        old_image = ""
        #revisa si tiene foto
        if request.user.photo:
            #path de la foto
            old_image = request.user.photo.path
        #formulario
        form = Update_user(request.POST,request.FILES, instance=usuario)
        #si el formato es valido
        if form.is_valid():
            photo_new = form.cleaned_data.get("photo")      
            if( (photo_new != request.user.photo.name)):
                #si esta, eliminar la foto vieja
                if os.path.exists(old_image) and (request.user.photo.name != "autentificacion/gato.jpg"):
                    #remove la foto vieja
                    os.remove(old_image)
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect("perfil")
    else:
        form = Update_user(instance=usuario)

    return render(request, "autentificacion/configuracion.html", {"categorias":categorias, "form": form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'autentificacion/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('perfil')

class crear_publicacion(View):

    def get(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion(request.POST,request.FILES)
        return render(request, "Autentificacion/crear_publicacion.html", {"categorias":categorias,"form":form})
        
    def post(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion(request.POST,request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect("perfil")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            return render(request, "Autentificacion/crear_publicacion.html", {"categorias":categorias,"form":form})