from django.db import models
from productos.models import Producto

class Proveedor(models.Model):
    rif = models.CharField(max_length=15, help_text="rif del proveedor")
    nombre = models.CharField(max_length=30, help_text="nombre del proveedor")
    telefono = models.CharField(max_length=15, null=True,
                                help_text="telefono del proveedor")
    direccion = models.CharField(max_length=80, null=True,
                                 help_text="direccion del proveedor")
    ultimo_pedido = models.DateField(help_text="Fecha del ultimo pedido al proveedor",
                                     null=True)

class Compra(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="codigo de la compra")
    proveedor = models.ForeignKey(Proveedor, related_name="compras",
                                  help_text="proveedor de la compra",
                                  on_delete=models.CASCADE)
    total = models.FloatField(null=True, default=0,
                              help_text="Monto total de la compra")
    fecha = models.DateField(help_text="Fecha de la compra")

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name="detalles",
                               help_text="compra a la que pertenece",
                               on_delete=models.CASCADE)
    cantidad = models.FloatField(help_text="cantidad de entrada")
    producto = models.ForeignKey(Producto, related_name="detalles",
                                 help_text="producto", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, help_text="Fecha de la venta")