from django.db import models
from productos.models import Producto

class Cliente(models.Model):
    rif = models.CharField(max_length=15, help_text="Rif/CI del cliente")
    nombre = models.CharField(max_length=30, help_text="Nomrbe del cliente")
    telefono = models.CharField(max_length=15, help_text="Telefono del cliente",
                                null=True)
    direccion = models.CharField(max_length=80, null=True,
                                 help_text="Direccion del cliente")

    def __str__(self):
      return self.nombre

class Salida(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="codigo de la salida")
    cliente = models.ForeignKey(Cliente, related_name="salidas",
                                  help_text="cliente de la salida",
                                  on_delete=models.CASCADE)
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
