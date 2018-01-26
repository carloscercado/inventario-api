from django.db import models
from decimal import Decimal

class Categoria(models.Model):
    codigo = models.CharField(max_length=64, help_text="codigo de la categoria", unique=True)
    nombre = models.CharField(unique=True, max_length=30, help_text="nombre de categoria")
    eliminable = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    LTS = "Lts"
    KG = "Kgs"
    UNI = "Unds"
    MTR = "Mts"
    MEDIDAS = (
        (LTS, LTS),
        (KG, KG),
        (UNI, UNI),
        (MTR, MTR)
        )
    codigo = models.CharField(max_length=64, help_text="codigo del producto", unique=True)
    nombre = models.CharField(max_length=30, help_text="nombre del producto")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT,
                                  help_text="Categoria del producto",
                                  related_name="productos")
    cantidad = models.FloatField(default=0, help_text="cantidad disponible")
    #cantidad_transito = models.FloatField(default=0, help_text="cantidad en transito")
    medida = models.CharField(choices=MEDIDAS, max_length=15, help_text="unidad de medida")
    minimo = models.FloatField(default=0, help_text="cantidad minima aceptable")
    #precio = models.DecimalField(max_digits=16, decimal_places=8,
    #                             default=Decimal(0), null=True,
    #                             help_text="precio del producto")