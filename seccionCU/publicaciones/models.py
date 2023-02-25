from django.db import models
from autentificacion.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name='categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre

class Publicaciones(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    imagen =  models.ImageField(upload_to='publicaciones', null=True, blank=True)
    estado = models.BooleanField(default=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=2, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name='publicacion'
        verbose_name_plural = 'publicaciones'

    def __str__(self):
        return self.titulo
    
class Solicitudes(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    valoracion = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
