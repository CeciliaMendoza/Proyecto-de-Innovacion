from django.db import models
from autentificacion.models import User
from django.db.models import Avg

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
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name='publicacion'
        verbose_name_plural = 'publicaciones'

    def __str__(self):
        return self.titulo
    @property
    def get_image_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        else:
            return "" 
        
    def average_rating(self):
        return Puntuacion.objects.filter(publicacion=self).aggregate(Avg("valoracion"))["valoracion__avg"] or 0

    def is_estado(self):
        if self.estado:
            return "Disponible"
        return "No disponible"

class Solicitudes(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)

class Puntuacion(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valoracion = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.publicacion.titulo}: {self.valoracion}"