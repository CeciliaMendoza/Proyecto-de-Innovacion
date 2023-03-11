from django.urls import path
from publicaciones import views

urlpatterns = [
    path("", views.principal, name="home"),
    path("search/", views.busquedas, name = "buquedas"),
    path("categoria/<int:categoria_id>/", views.categoria, name="categoria"),

]