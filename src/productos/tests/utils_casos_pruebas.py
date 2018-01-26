from inventario.api_casos_pruebas import APICasoPrueba
from productos.models import Categoria, Producto
from ubicacion.models import Unidad
from ubicacion.tests import utils_casos_pruebas
from django.contrib.auth.models import User
from personas.models import Persona
import uuid

class UtilCasosPrueba(APICasoPrueba):
    
    def setUp(self):
        user = User(username="admin", email="admin@admin.admin")
        user.set_password("admin")
        user.save()
        self.usuario = Persona.objects.create(user=user, nombre="Carlos",
                                              apellido="Cercado", direccion="tacal",
                                              telefono="034343", pregunta="abc",
                                              respuesta="abc", cargo="USER")
        self.client.credentials(HTTP_AUTHORIZATION='Basic YWRtaW5AYWRtaW4uYWRtaW46YWRtaW4=')

    def registrar_categoria(self, nombre):
        categoria = Categoria(nombre=nombre, codigo=uuid.uuid4())
        categoria.save()
        return categoria

    def registrar_producto(self, categoria_nombre="mi categoria"):
        categoria = self.registrar_categoria(categoria_nombre)
        producto = Producto(nombre="Mi producto", categoria=categoria,
                            medida=Producto.KG, codigo=uuid.uuid4())
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
        User.objects.all().delete()
        super().tearDown()