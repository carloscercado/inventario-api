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

class Venta(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="codigo de la venta")
    cliente = models.ForeignKey(Cliente, related_name="ventas",
                                  help_text="cliente de la venta",
                                  on_delete=models.CASCADE)
    total = models.FloatField(null=True, default=0,
                              help_text="Monto total de la venta")
    fecha = models.DateField(help_text="Fecha de la venta")

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles",
                               help_text="venta a la que pertenece",
                               on_delete=models.CASCADE)
    cantidad = models.FloatField(help_text="cantidad de salida")
    producto = models.ForeignKey(Producto, related_name="salidas",
                                 help_text="producto", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, help_text="Fecha de la compra")
