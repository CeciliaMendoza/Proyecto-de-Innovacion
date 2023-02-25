from django.shortcuts import render

# Create your views here.

def principal(request):
    return render(request, "publicaciones/home.html")

def busquedas(request):
    return render(request, "publicaciones/index.html")