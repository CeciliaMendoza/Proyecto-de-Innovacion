from django import forms
from django.forms import ModelForm
from publicaciones.models import Publicaciones
from django.utils.translation import gettext_lazy as _

class Crear_publicacion_form(ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['titulo', 'descripcion', 'precio','estado', 'categoria', 'imagen']
        exclude = ['autor']
        labels = {
            'estado': _('Disponible'),
        }

class Update_publicacion_form(ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['titulo', 'descripcion', 'precio','estado', 'categoria', 'imagen']
        exclude = ['autor']

        labels = {
            'estado': _('Disponible'),
        }