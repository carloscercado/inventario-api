from inventario.api_casos_pruebas import APICasoPrueba
from salidas.models import Dependencia, Salida
from productos.models import Categoria, Producto
import datetime

class UtilCasosPrueba(APICasoPrueba):

    def registrar_dependencia(self):
        dependencia = Dependencia(nombre="Paulo milanes",
                                  telefono="02934163378", direccion="mi direccion")
        dependencia.save()
        return dependencia

    def tearDown(self):
        Dependencia.objects.all().delete()
        super().tearDown()
