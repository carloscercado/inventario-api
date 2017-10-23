from django.db import models
from productos.models import Producto
from decimal import Decimal

class Proveedor(models.Model):
    rif = models.CharField(max_length=15, help_text="rif del proveedor")
    nombre = models.CharField(max_length=30, help_text="nombre del proveedor")
    telefono = models.CharField(max_length=15, null=True,
                                help_text="telefono del proveedor")
    direccion = models.CharField(max_length=80, null=True,
                                 help_text="direccion del proveedor")
    ultimo_pedido = models.DateField(help_text="Fecha del ultimo pedido al proveedor",
                                     null=True)

    def __str__(self):
      return self.nombre

class Compra(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="codigo de la compra")
    proveedor = models.ForeignKey(Proveedor, related_name="compras",
                                  help_text="proveedor de la compra",
                                  on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=16, decimal_places=8,
                                default=Decimal(0), null=True,
                                help_text="Monto total de la compra")
    fecha = models.DateField(help_text="Fecha de la compra")

    @property
    def bloqueada(self):
        for i in self.detalles.all():
            if i.faltante_por_procesar != i.cantidad:
                return True
        return False

    @property
    def procesada(self):
        for i in self.detalles.all():
            if not i.procesado:
                return False
        return True

    @property
    def eliminable(self):
        return not self.bloqueada

    def borrar_detalles(self):
      DetalleCompra.objects.filter(compra_id=self.id).delete()

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name="detalles",
                               help_text="compra a la que pertenece",
                               on_delete=models.CASCADE)
    cantidad = models.FloatField(help_text="cantidad de entrada")
    producto = models.ForeignKey(Producto, related_name="detalles",
                                 help_text="producto", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, help_text="Fecha de la venta")
    precio = models.DecimalField(max_digits=16, decimal_places=8,
                                 help_text="Precio unitario del producto")
    cantidad_procesada = models.FloatField(help_text="cantidad de procesada", default=0)

    @property
    def total(self):
        return self.precio * Decimal(self.cantidad)

    @property
    def faltante_por_procesar(self):
        return self.cantidad - self.cantidad_procesada

    @property
    def procesado(self):
        return (self.cantidad_procesada == self.cantidad)

    def __str__(self):
      return str(self.id) + "-" + self.producto.nombre