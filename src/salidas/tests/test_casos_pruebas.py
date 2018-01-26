from .utils_casos_pruebas import UtilCasosPrueba
from salidas.models import Dependencia, Salida
import uuid
from productos.models import Producto
from compras.tests import utils_casos_pruebas as compras
from ubicacion.tests import utils_casos_pruebas as ubicacion
import pdb

class CasosPruebas(UtilCasosPrueba):

    """
    ********************
    ******Salidas******
    ********************
    """

    def test_registrar_dependencia(self):
        """
        Prueba el registro de un dependencia
        """
        payload = {
            "nombre": "Mi dependencia",
            "direccion": "mi direccion",
            "telefono": "0293144726"
        }
        respuesta = self.client.post("/dependencias", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)


    def test_modificar_dependencia(self):
        """
        Prueba modificar un dependencia
        """
        dependencia = self.registrar_dependencia()
        payload = {
            "nombre": "Mi dependencia 2",
            "direccion": "mi direccion",
            "telefono": "0293144726"
        }
        _id = str(dependencia.id)
        respuesta = self.client.put("/dependencias/" + _id, payload, format="json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], dependencia.id)
        self.assertNotEqual(respuesta.json()["nombre"], dependencia.nombre)

    def test_eliminar_dependencia(self):
        """
        Prueba eliminar un dependencia
        """
        dependencia = self.registrar_dependencia()
        _id = str(dependencia.id)
        respuesta = self.client.delete("/dependencias/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Dependencia.objects.filter(id=dependencia.id).first(), None)

    def test_buscar_dependencia(self):
        """
        Prueba buscar un dependencia
        """
        dependencia = self.registrar_dependencia()
        _id = str(dependencia.id)
        respuesta = self.client.get("/dependencias/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], dependencia.id)

    def test_listar_dependencia(self):
        """
        Prueba listar dependencias
        """
        self.registrar_dependencia()
        self.registrar_dependencia()

        respuesta = self.client.get("/dependencias")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)





    def test_registrar_salida_vacia(self):
        """
        Prueba registrar una salida sin productos
        """

        dependencia = self.registrar_dependencia()
        payload = {
            "fecha": "2017-01-02",
            "dependencia": dependencia.id,
            "detalles": []
        }
        respuesta = self.client.post("/salidas", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(len(respuesta.json().get("codigo")), 32)
        self.assertEqual(len(respuesta.json().get("detalles")), 0)

    def test_registrar_salida_producto_cero(self):
        """
        Prueba registrar una salida usando un producto escaso
        """

        dependencia = self.registrar_dependencia()

        clase = compras.UtilCasosPrueba()
        producto = clase.registrar_producto()

        payload = {
            "fecha": "2017-01-02",
            "dependencia": dependencia.id,
            "detalles": [
                {
                    "producto": producto.id,
                    "cantidad": 1
                }
            ]
        }
        respuesta = self.client.post("/salidas", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json().get("detalles")[0], None)

    def test_registrar_salida(self):
        """
        Prueba registrar una salida
        """

        clase = compras.UtilCasosPrueba()

        producto = clase.registrar_producto()

        compra = clase.registrar_compra_con_detalles(producto=producto, usuario=self.usuario)
        detalle1 = compra.detalles.all().first()

        ubi = ubicacion.UtilCasosPrueba()

        seccion = ubi.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 500,
            "altura": 500,
            "ancho": 500,
            "cantidad": 2
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        dependencia = self.registrar_dependencia()

        payload = {
            "fecha": "2017-01-02",
            "dependencia": dependencia.id,
            "detalles": [
                {
                    "producto": producto.id,
                    "cantidad": 2
                }
            ]
        }
        respuesta = self.client.post("/salidas", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        producto = Producto.objects.filter(id=producto.id).get()
        self.assertEqual(producto.cantidad, 0)

    def test_registrar_salida_mayor_disponible(self):
        """
        Prueba registrar una salida de un producto mayor al disponible
        """

        clase = compras.UtilCasosPrueba()

        producto = clase.registrar_producto()

        compra = clase.registrar_compra_con_detalles(cantidad=15, producto=producto, usuario=self.usuario)
        detalle1 = compra.detalles.all().first()

        ubi = ubicacion.UtilCasosPrueba()

        seccion = ubi.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 20,
            "altura": 20,
            "ancho": 20,
            "cantidad": 15
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        dependencia = self.registrar_dependencia()

        payload = {
            "fecha": "2017-01-02",
            "dependencia": dependencia.id,
            "detalles": [
                {
                    "producto": producto.id,
                    "cantidad": 16
                }
            ]
        }
        respuesta = self.client.post("/salidas", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)

        producto = Producto.objects.filter(id=producto.id).get()
        self.assertEqual(producto.cantidad, 15)

    def test_listar_salidas(self):

        self.test_registrar_salida()

        respuesta = self.client.get("/salidas", format="json")
        self.assertEqual(len(respuesta.json()), 1)
        self.assertEqual(respuesta.status_code, 200)

    def test_buscar_salidas(self):

        self.test_registrar_salida()

        respuesta = self.client.get("/salidas/1", format="json")
        self.assertEqual(len(respuesta.json().get("detalles")), 1)
        self.assertEqual(respuesta.status_code, 200)

    def test_eliminar_salidas(self):

        self.test_registrar_salida()
        respuesta = self.client.get("/salidas")
        primera = respuesta.json()[0]

        respuesta = self.client.delete("/salidas/" + str(primera.get("id")))
        self.assertEqual(respuesta.status_code, 400)

    def test_modificar_salidas(self):

        self.test_registrar_salida()

        respuesta = self.client.get("/salidas")
        primera = respuesta.json()[0]

        payload = {
            "fecha": "2017-01-02",
        }

        respuesta = self.client.put("/salidas/" + str(primera.get("id")), payload, format="json")
        self.assertEqual(respuesta.status_code, 400)

