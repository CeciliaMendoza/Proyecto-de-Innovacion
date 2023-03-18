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

    publicacion = Publicaciones.objects.get(id=publicacion_id)
    if request.method == 'POST':
        form = Update_publicacion_form(request.POST,request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = Update_publicacion_form(instance=publicacion)

    return render(request, "publicaciones/update_publicacion.html", {"categorias":categorias, "form": form})

def delete_publicacion(request, publicacion_id):
    try:
        publicacion = Publicaciones.objects.get(id=publicacion_id)
        publicacion.delete()
    except Exception as e:
        print(e.message)
    return redirect("perfil")