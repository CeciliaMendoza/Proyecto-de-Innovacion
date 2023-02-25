from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    birthdate = models.DateField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=200, null=True)
    photo = models.ImageField(null=True)
    career = models.CharField(max_length=30,null=True)
    created = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username