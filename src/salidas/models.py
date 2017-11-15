from django.db import models
from productos.models import Producto

class Dependencia(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nomrbe de la dependencia")
    telefono = models.CharField(max_length=15, help_text="Telefono de la dependencia",
                                null=True)
    direccion = models.CharField(max_length=80, null=True,
                                 help_text="Direccion de la dependencia")
    descripcion = models.CharField(max_length=80, null=True,
                                 help_text="Descripcion breve de la dependencia")

    def __str__(self):
      return self.nombre

class Salida(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="codigo de la salida")
    dependencia = models.ForeignKey(Dependencia, related_name="salidas",
                                  help_text="cliente de la salida",
                                  on_delete=models.CASCADE, default=0)
    total = models.FloatField(default=0,
                              help_text="Monto total de la salida")
    fecha = models.DateField(help_text="Fecha de la salida")


    def borrar_detalles(self):
        DetalleVenta.objects.filter(venta_id=self.id).delete()

class DetalleVenta(models.Model):
    salida = models.ForeignKey(Salida, related_name="detalles",
                               help_text="salida a la que pertenece",
                               on_delete=models.CASCADE)
    cantidad = models.FloatField(help_text="cantidad de salida")
    producto = models.ForeignKey(Producto, related_name="salidas",
                                 help_text="producto", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, help_text="Fecha de la compra")
