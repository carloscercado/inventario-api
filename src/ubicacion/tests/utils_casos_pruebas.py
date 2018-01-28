from inventario.api_casos_pruebas import APICasoPrueba
from ubicacion.models import Almacen, Seccion, Unidad
from compras.tests import utils_casos_pruebas
from compras.models import Compra
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

    def registrar_almacen(self):
        almacen = Almacen(nombre="mi almacen", direccion="mi direccion",
                          telefono="292-4333323", eliminable=True, codigo=uuid.uuid4().hex)
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

    def registrar_compra_con_detalles(self, codigo=None, categoria_nombre="mi categoria", usuario=None):
        clase = utils_casos_pruebas.UtilCasosPrueba()
        usuario = self.usuario if usuario is None else usuario
        return clase.registrar_compra_con_detalles(codigo, categoria_nombre=categoria_nombre, usuario=usuario)

    def registrar_unidad(self, longi, ancho, alto, codigo=None, categoria_nombre="Mi categoria"):
        codigo = uuid.uuid4().hex if codigo is None else codigo
        compra = self.registrar_compra_con_detalles(codigo, categoria_nombre=categoria_nombre)
        detalle1 = compra.detalles.all()[0]
        seccion = self.registrar_seccion()
        unidad = Unidad(altura=alto, ancho=ancho, longitud=longi,
                        unidad=detalle1, seccion=seccion, codigo=codigo,
                        fecha=compra.fecha, producto=detalle1.producto.id)
        unidad.save()
        return unidad


    def tearDown(self):
        Seccion.objects.all().delete()
        Almacen.objects.all().delete()
        Compra.objects.all().delete()
        Unidad.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()