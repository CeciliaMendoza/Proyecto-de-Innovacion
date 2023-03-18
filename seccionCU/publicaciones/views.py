from django.shortcuts import render, redirect
from .models import Categoria, Publicaciones
from django.core.paginator import Paginator
from publicaciones.forms import Crear_publicacion_form, Update_publicacion_form
import os
from django.contrib import messages
from django.views.generic import View
# Create your views here.

def principal(request):
    publicaciones_all = Publicaciones.objects.all()
    categorias = Categoria.objects.all()
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 6) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

def categoria(request, categoria_id):
    categorias = Categoria.objects.all()
    #categoria seleccionada
    categoria = Categoria.objects.get(id=categoria_id)
    publicaciones_all = Publicaciones.objects.filter(categoria=categoria)
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 6) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

def busquedas(request):
    categorias = Categoria.objects.all()
    if request.method == "GET":
        #busqueda
        query = request.GET.get('busqueda')
        #buscar sobre el campo titulo
        publicaciones_all= Publicaciones.objects.filter(titulo__contains=query)
        # Show 5 contacts per page.
        paginator = Paginator(publicaciones_all, 6) 
        #obtiene el numeor de pagina 
        page_number = request.GET.get('page')
        publicaciones = paginator.get_page(page_number)
    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

class crear_publicacion(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion_form(request.POST,request.FILES)
        return render(request, "publicaciones/crear_publicacion.html", {"categorias":categorias,"form":form})
        
    def post(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion_form(request.POST,request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect("perfil")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            return render(request, "publicaciones/crear_publicacion.html", {"categorias":categorias,"form":form})
        
def update_publicacion(request, publicacion_id):
    categorias = Categoria.objects.all()

    usuario = Publicaciones.objects.get(id=publicacion_id)

    if request.method == 'GET':
        """       
        #imagen antigua
        old_image = ""
        #revisa si tiene foto
        if request.user.photo:
            #path de la foto
            old_image = request.user.photo.path
        #formulario
        form = Update_publicacion_form(request.POST,request.FILES, instance=usuario)
        #si el formato es valido
        if form.is_valid() :
            if(form.cleaned_data.get("photo")  != request.user.photo.name):
                #si esta, eliminar la foto vieja
                if os.path.exists(old_image):
                    if request.user.photo.name != "autentificacion/gato.jpg":
                        #remove la foto vieja
                        os.remove(old_image)
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect("perfil")
        """
        form = Update_publicacion_form(request.POST,request.FILES, instance=usuario)
        print("sdsd")
    else:
        form = Update_publicacion_form(instance=usuario)

    return render(request, "autentificacion/configuracion.html", {"categorias":categorias, "form": form})
