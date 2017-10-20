from django.db import models
from compras.models import DetalleCompra

class Almacen(models.Model):
    nombre = models.CharField(max_length=30, help_text="nombre del almacen")
    direccion = models.CharField(max_length=60, help_text="direccion del almacen")
    telefono = models.CharField(null=True, max_length=15,
                                help_text="telefono de comunicacion")

    def __str__(self):
        return self.nombre

class Estante(models.Model):
    nombre = models.CharField(max_length=30, help_text="nombre del almacen")
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE,
                                  help_text="Almacen al que pertenece",
                                  related_name="estantes")
    capacidad_total = models.FloatField(default=0, help_text="capacidad del almacen")
    capacidad_restante = models.FloatField(help_text="capacidad disponible en el almacen")

class Unidad(models.Model):
    unidad = models.ForeignKey(DetalleCompra, related_name="unidades",
                               help_text="producto a ubicar",
                               on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30, help_text="codigo unico de la unidad")
    estado = models.BooleanField(default=True, null=True, help_text="Disponible/Usado")
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE,
                                help_text="Estante donde se ubicará la unidad",
                                related_name="unidades")