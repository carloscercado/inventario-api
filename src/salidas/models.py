from django.db import models
from productos.models import Producto
from ubicacion.models import Unidad
from personas.models import Persona

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
    codigo = models.CharField(max_length=32, unique=True,
                              help_text="codigo de la salida")
    dependencia = models.ForeignKey(Dependencia, related_name="salidas",
                                  help_text="cliente de la salida",
                                  on_delete=models.CASCADE, default=0)
    total = models.FloatField(default=0,
                              help_text="Monto total de la salida")
    fecha = models.DateField(help_text="Fecha de la salida")
    usuario = models.ForeignKey(Persona, related_name="compras_2",
                                 help_text="usuario que registro la compra",
                                 on_delete=models.CASCADE)

    @property
    def eliminable(self):
        return self.detalles.all().count() == 0


    def borrar_detalles(self):
        self.detalles.all().delete()

    def aplicar_metodo_fifo(self):
        """
        Algoritmo para aplicar el metodo FIFO en
        las salidas de los productos.
        """
        detalles = self.detalles.all()

        for i in detalles:
            total = i.cantidad
            contador = 0
            unidades = Unidad.objects.filter(producto=i.producto.id).order_by('-fecha')

            for unidad in unidades.all():
                unidad.estado = False
                unidad.save()

                pro = Producto.objects.filter(id=unidad.producto).first()
                pro.cantidad = (pro.cantidad - 1)
                pro.save()

                seccion = unidad.seccion
                seccion.volumen_restante = (seccion.volumen_restante - unidad.volumen)
                seccion.save()
                contador = contador + 1
                if contador == total:
                    break

class DetalleSalida(models.Model):
    salida = models.ForeignKey(Salida, related_name="detalles",
                               help_text="salida a la que pertenece",
                               on_delete=models.CASCADE)
    cantidad = models.FloatField(help_text="cantidad de salida")
    producto = models.ForeignKey(Producto, related_name="salidas",
                                 help_text="producto", on_delete=models.CASCADE)
    fecha = models.DateField(null=True, help_text="Fecha de la compra")
