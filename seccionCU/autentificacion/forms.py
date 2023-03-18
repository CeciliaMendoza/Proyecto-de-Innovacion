from django import forms
from autentificacion.models import User
from publicaciones.models import Publicaciones
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'career', 'email')
        labels = {
            'username': _('Nombre de usuario'),
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'career': _('Carrera'),

        }

    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  


class Update_user(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','career', 'birthdate', 'address','phone', "photo"]
        labels = {
            'username': _('Nombre de usuario'),
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'career': _('Carrera'),
            'birthdate': _('Fecha de nacimiento'),
            'phone': _('Telefono'),
            'address': _('Direccion'),
            'photo': _('Foto'),
        }
        widgets = {
            'birthdate': forms.DateInput(format=('%Y-%m-%d'),attrs={'type': 'date'}),
        }


class Crear_publicacion(ModelForm):

    class Meta:
        model = Publicaciones
        fields = ['titulo', 'descripcion', 'precio','estado', 'categoria', 'imagen']
        exclude = ['autor']


