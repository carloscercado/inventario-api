from rest_framework.test import APITestCase
from ubicacion.models import Almacen, Seccion

class UtilCasosPrueba(APITestCase):

    def registrar_almacen(self):
        almacen = Almacen(nombre="mi almacen", direccion="mi direccion",
                          telefono="02924333323", eliminable=True)
        almacen.save()
        return almacen

    def registrar_seccion(self):
        almacen = self.registrar_almacen()
        seccion = Seccion(nombre="Mi seccion", almacen=almacen,
                          altura=1000, anchura=1000,
                          longitud=1000)
        seccion.volumen_restante = seccion.volumen
        almacen.eliminable = False

        almacen.save()
        seccion.save()
        return seccion

    def tearDown(self):
        Seccion.objects.all().delete()
        Almacen.objects.all().delete()