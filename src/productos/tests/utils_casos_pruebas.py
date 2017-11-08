from rest_framework.test import APITestCase
from productos.models import Categoria

class UtilCasosPrueba(APITestCase):

    def registrar_categoria(self, nombre):
        categoria = Categoria(nombre=nombre)
        categoria.save()
        return categoria