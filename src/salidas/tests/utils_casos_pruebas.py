from inventario.api_casos_pruebas import APICasoPrueba
from salidas.models import Dependencia, Salida
from productos.models import Categoria, Producto
import datetime
from personas.models import Persona
from django.contrib.auth.models import User

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

    def registrar_dependencia(self):
        dependencia = Dependencia(nombre="Paulo milanes",
                                  telefono="02934163378", direccion="mi direccion")
        dependencia.save()
        return dependencia

    def tearDown(self):
        Dependencia.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()
