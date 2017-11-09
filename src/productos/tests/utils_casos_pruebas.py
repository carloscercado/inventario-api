from rest_framework.test import APITestCase
from productos.models import Categoria, Producto

class UtilCasosPrueba(APITestCase):

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

    def tearDown(self):
        Producto.objects.all().delete()
        Categoria.objects.all().delete()