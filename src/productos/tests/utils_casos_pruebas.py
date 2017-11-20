from inventario.api_casos_pruebas import APICasoPrueba
from productos.models import Categoria, Producto
from ubicacion.models import Unidad
from ubicacion.tests import utils_casos_pruebas

class UtilCasosPrueba(APICasoPrueba):

    def registrar_categoria(self, nombre):
        categoria = Categoria(nombre=nombre)
        categoria.save()
        return categoria

    def registrar_producto(self, categoria_nombre="mi categoria"):
        categoria = self.registrar_categoria(categoria_nombre)
        producto = Producto(nombre="Mi producto", categoria=categoria,
                            medida=Producto.KG)
        categoria.eliminable = False
        categoria.save()
        producto.save()
        return producto

    def registrar_compra_con_detalles(self, codigo=None, categoria_nombre="mi categoria"):
        clase = utils_casos_pruebas.UtilCasosPrueba()
        return clase.registrar_compra_con_detalles(codigo, categoria_nombre=categoria_nombre, usuario=self.usuario)

    def tearDown(self):
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        super().tearDown()