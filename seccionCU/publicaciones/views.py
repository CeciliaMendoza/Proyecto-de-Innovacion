from django.shortcuts import render
from .models import Categoria, Publicaciones
from django.core.paginator import Paginator

# Create your views here.

def principal(request):

    publicaciones_all = Publicaciones.objects.all()
    categorias = Categoria.objects.all()
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 5) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

def categoria(request, categoria_id):
    publicaciones_all = Publicaciones.objects.all()
    categorias = Categoria.objects.all()
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 5) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

def busquedas(request):
    #doesnt work yet
    publicaciones_all = Publicaciones.objects.all()
    categorias = Categoria.objects.all()
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 5) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})
