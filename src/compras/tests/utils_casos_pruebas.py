from inventario.api_casos_pruebas import APICasoPrueba
from compras.models import Proveedor, Compra, DetalleCompra
from productos.models import Categoria, Producto
import datetime
from personas.models import Persona
from django.contrib.auth.models import User
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

    def registrar_proveedor(self):
        proveedor = Proveedor(rif="23923164", nombre="Paulo milanes",
                              telefono="02934163378", direccion="mi direccion")
        proveedor.save()
        return proveedor

    def registrar_producto(self, categoria_nombre="mi categoria"):
        categoria = Categoria(nombre=categoria_nombre, codigo=uuid.uuid4())
        categoria.save()
        producto = Producto(nombre="Mi producto", categoria=categoria,
                            medida=Producto.KG, codigo=uuid.uuid4())
        categoria.eliminable = False
        categoria.save()
        producto.save()
        return producto

    def registrar_compra(self, codigo=None):
        if codigo is None:
            codigo = "000001"
        fecha = datetime.datetime.now()

        compra = Compra(codigo=codigo, fecha=fecha,
                        proveedor=self.registrar_proveedor(),
                        usuario=self.usuario)
        compra.save()
        return compra

    def registrar_compra_con_detalles(self, codigo=None, usuario=None, producto=None, cantidad=2, categoria_nombre="mi categoria"):
        if codigo is None:
            codigo = uuid.uuid4()
        fecha = datetime.datetime.now()

        if usuario is None:
            usuario = self.usuario
        compra = Compra(codigo=codigo, fecha=fecha,
                        proveedor=self.registrar_proveedor(),
                        usuario=usuario)
        compra.save()
        if producto is None:
            producto = self.registrar_producto(categoria_nombre=categoria_nombre)
        detalle = DetalleCompra(fecha=compra.fecha, cantidad=cantidad, producto=producto,
                                precio=1000, compra=compra)
        detalle2 = DetalleCompra(fecha=compra.fecha, cantidad=4, producto=producto,
                                 precio=500, compra=compra)
        detalle.save()
        detalle2.save()
        return compra

    def tearDown(self):
        Proveedor.objects.all().delete()
        Compra.objects.all().delete()
        User.objects.all().delete()
        super().tearDown()