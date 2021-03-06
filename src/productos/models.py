from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=30, help_text="nombre de categoria")

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
    nombre = models.CharField(max_length=30, help_text="nombre del producto")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,
                                  help_text="Categoria del producto",
                                  related_name="productos")
    cantidad = models.FloatField(default=0, help_text="cantidad disponible")
    medida = models.CharField(choices=MEDIDAS, max_length=15, help_text="unidad de medida")
    minimo = models.FloatField(default=0, help_text="cantidad minima aceptable")