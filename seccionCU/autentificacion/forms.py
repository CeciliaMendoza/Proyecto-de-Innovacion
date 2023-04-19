from django import forms
from autentificacion.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.core.validators import RegexValidator
import re 

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'career', 'email')
        labels = {
            'username': _('Nombre de usuario'),
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'career': _('Carrera'),

        }

    def clean_email(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        regex = r"@alumnos\.uacj\.mx$"

        if new.count():  
            raise forms.ValidationError("Este email ya esta registrado")
        matches = re.search(regex, email)
        if not matches:
            print(matches)
            print("no matches")
            raise forms.ValidationError("Debe ser un correo institucional")
        
        return email  
    def clean_password1(self):
                
        password1 = self.cleaned_data.get("password1")
        if not re.findall('[A-Z]', password1):
            raise forms.ValidationError("La contraseña debe tener al menos una letra mayuscula, A-Z.")
        if not re.findall('[0-9]', password1):
            raise forms.ValidationError("La contraseña debe tener al menos un digito, 0-9.")
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña debe contener al menos 8 caracteres.")
        return password1
    
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