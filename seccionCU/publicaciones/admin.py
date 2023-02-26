from django.contrib import admin
from publicaciones.models import Categoria, Publicaciones, Solicitudes, Puntuacion
# Register your models here.
class Categoria_admin(admin.ModelAdmin):
    readonly_fields=("created", "updated")
class Publicaciones_admin(admin.ModelAdmin):
    readonly_fields=("created", "updated")
class Solicitudes_admin(admin.ModelAdmin):
    readonly_fields=("created", "updated")
class Puntuacion_admin(admin.ModelAdmin):
    readonly_fields=("created", "updated")

admin.site.register(Categoria, Categoria_admin)
admin.site.register(Publicaciones, Publicaciones_admin)
admin.site.register(Solicitudes, Solicitudes_admin)
admin.site.register(Puntuacion, Puntuacion_admin)
