from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    Path = models.CharField(max_length=150, null=True)
    estado = models.CharField(max_length=50, null=True)
    
class Sitios(models.Model):
    dominio = models.CharField(max_length=50, null=True)
    subDominio = models.CharField(max_length=50, null=True)
    completo = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    