from rest_framework.test import APITestCase
from ubicacion.models import Almacen, Estante

class UtilCasosPrueba(APITestCase):

    def registrar_almacen(self, nombre):
        almacen = Almacen(nombre="mi almacen", direccion="mi direccion",
                          telefono="02924333323")
        almacen.save()
        return almacen

    def registrar_estante(self):
        almacen = self.registrar_almacen()
        estante = Estante(nombre="Mi estante", almacen=almacen,
                          medida=Producto.KG)
        almacen.eliminable = False
        almacen.save()
        estante.save()
        return estante

    def tearDown(self):
        Estante.objects.all().delete()
        Almacen.objects.all().delete()