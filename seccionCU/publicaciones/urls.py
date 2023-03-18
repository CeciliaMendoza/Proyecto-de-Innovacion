from django.urls import path
from publicaciones import views
from publicaciones.views import crear_publicacion
urlpatterns = [
    path("", views.principal, name="home"),
    path("categoria/<int:categoria_id>/", views.categoria, name="categoria"),
    path("busqueda/", views.busquedas, name="busqueda"),
    path("create/", crear_publicacion.as_view(), name="create"),
    path("update/<int:publicacion_id>", views.update_publicacion, name="update"),
    path("delete/<int:publicacion_id>", views.delete_publicacion, name="delete"),

]

