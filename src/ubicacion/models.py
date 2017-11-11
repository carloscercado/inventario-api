from django.db import models
from compras.models import DetalleCompra
from productos.models import Producto

class Almacen(models.Model):
    nombre = models.CharField(max_length=30, help_text="nombre del almacen")
    direccion = models.CharField(max_length=60, help_text="direccion del almacen")
    telefono = models.CharField(null=True, max_length=15,
                                help_text="telefono de comunicacion")
    eliminable = models.BooleanField(default=True)

    @property
    def volumen(self):
        total = 0
        for i in self.secciones.all():
            total = total + i.capacitad_total
        return total

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=30, help_text="nombre del almacen")
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE,
                                  help_text="Almacen al que pertenece",
                                  related_name="secciones")
    volumen_restante = models.FloatField(default=0,
                                           help_text="capacidad disponible en el almacen")
    longitud = models.FloatField(help_text="longitud del almacen")
    anchura =  models.FloatField(help_text="anchura del almacen")
    altura = models.FloatField(help_text="altura del almacen")

    @property
    def volumen(self):
        return self.longitud * self.anchura * self.altura

    def __str__(self):
      return self.nombre

class Unidad(models.Model):
    unidad = models.ForeignKey(DetalleCompra, related_name="unidades",
                               help_text="producto a ubicar",
                               on_delete=models.CASCADE)
    codigo = models.CharField(max_length=64, help_text="codigo unico de la unidad")
    estado = models.BooleanField(default=True, help_text="Disponible/Usado")
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE,
                                help_text="Estante donde se ubicará la unidad",
                                related_name="unidades")
    producto = models.IntegerField(default=0)
    fecha = models.DateField(help_text="Fecha de la ingreso")
    longitud = models.FloatField(help_text="longitud de la unidad")
    ancho =  models.FloatField(help_text="anchura de la unidad")
    altura = models.FloatField(help_text="altura de la unidad")

    @property
    def volumen(self):
        return self.longitud * self.anchura * self.altura