from rest_framework.test import APITestCase
from compras.models import Proveedor, Compra, DetalleCompra
from productos.models import Categoria, Producto
import datetime

class UtilCasosPrueba(APITestCase):

    def registrar_proveedor(self):
        proveedor = Proveedor(rif="23923164", nombre="Paulo milanes",
                              telefono="02934163378", direccion="mi direccion")
        proveedor.save()
        return proveedor

    def registrar_producto(self, categoria_nombre="mi categoria"):
        categoria = Categoria(nombre=categoria_nombre)
        categoria.save()
        producto = Producto(nombre="Mi producto", categoria=categoria,
                            medida=Producto.KG)
        categoria.eliminable = False
        categoria.save()
        producto.save()
        return producto

    def registrar_compra(self, codigo=None):
        if codigo is None:
            codigo = "000001"
        fecha = datetime.datetime.now()
        compra = Compra(codigo=codigo, fecha=fecha,
                        proveedor=self.registrar_proveedor())
        compra.save()
        return compra

    def registrar_compra_con_detalles(self, codigo=None, categoria_nombre="mi categoria"):
        if codigo is None:
            codigo = "000001"
        fecha = datetime.datetime.now()
        compra = Compra(codigo=codigo, fecha=fecha,
                        proveedor=self.registrar_proveedor())
        compra.save()
        producto = self.registrar_producto(categoria_nombre=categoria_nombre)
        detalle = DetalleCompra(fecha=compra.fecha, cantidad=2, producto=producto,
                                precio=1000, compra=compra)
        detalle2 = DetalleCompra(fecha=compra.fecha, cantidad=4, producto=producto,
                                 precio=500, compra=compra)
        detalle.save()
        detalle2.save()
        return compra

    def tearDown(self):
        Proveedor.objects.all().delete()
        Compra.objects.all().delete()