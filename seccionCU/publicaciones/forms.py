from django import forms
from django.forms import ModelForm
from publicaciones.models import Publicaciones
from django.utils.translation import gettext_lazy as _

class Crear_publicacion_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["estado"].widget.attrs['checked'] = "checked"
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Publicaciones
        fields = ['titulo', 'descripcion', 'precio','estado', 'categoria', 'imagen']
        exclude = ['autor']
        labels = {
            'estado': _('Disponible'),
        }

class Update_publicacion_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = Publicaciones
        fields = ['titulo', 'descripcion', 'precio', 'categoria','estado', 'imagen']
        exclude = ['autor']

        labels = {
            'estado': _('Disponible'),
        }