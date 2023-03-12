from django.urls import path
from publicaciones import views

urlpatterns = [
    path("", views.principal, name="home"),
    path("categoria/<int:categoria_id>/", views.categoria, name="categoria"),
    path("busqueda/", views.busquedas, name="busqueda"),
]