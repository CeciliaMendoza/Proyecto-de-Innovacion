from django.shortcuts import render
from .models import Categoria, Publicaciones
from django.core.paginator import Paginator

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
