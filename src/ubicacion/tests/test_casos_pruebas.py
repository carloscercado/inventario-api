from .utils_casos_pruebas import UtilCasosPrueba
from ubicacion.models import Almacen, Seccion, Unidad
import pdb

class CasosPruebas(UtilCasosPrueba):

    def test_registrar_almacen(self):
        """
        Prueba el registro de un almacen
        """
        payload = {
            "nombre": "Mi almacen",
            "direccion": "mi direccion",
            "telefono": "02934333333",
            "secciones": []
        }
        respuesta = self.client.post("/almacenes", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

    def test_registrar_almacen_con_seccion(self):
        """
        Prueba el registro de un almacen cin estantes
        """
        payload = {
            "nombre": "Mi almacen",
            "direccion": "mi direccion",
            "telefono": "02934333333",
            "secciones": [
                {
                    "nombre": "mi estante",
                    "anchura": 1000,
                    "altura": 1000,
                    "longitud": 1000
                },
                {
                    "nombre": "mi estante 2",
                    "anchura": 1000,
                    "altura": 1000,
                    "longitud": 1000
                }
            ]
        }
        respuesta = self.client.post("/almacenes", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(len(respuesta.json().get("secciones")), 2)

    def test_modificar_almacen(self):
        """
        Prueba modificar un almacen
        """
        almacen = self.registrar_almacen()
        payload = {
            "nombre": "Mi almacen 2",
            "direccion": "una direccion",
            "telefono": "02934164454",
            "secciones": []
        }
        _id = str(almacen.id)
        respuesta = self.client.put("/almacenes/" + _id, payload, format="json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], almacen.id)
        self.assertNotEqual(respuesta.json()["nombre"], almacen.nombre)

    def test_eliminar_almacen(self):
        """
        Prueba eliminar un almacen
        """
        almacen = self.registrar_almacen()
        _id = str(almacen.id)
        respuesta = self.client.delete("/almacenes/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Almacen.objects.filter(id=almacen.id).first(), None)

    def test_buscar_almacen(self):
        """
        Prueba buscar un almacen
        """
        almacen = self.registrar_almacen()
        _id = str(almacen.id)
        respuesta = self.client.get("/almacenes/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], almacen.id)

    def test_listar_almacen(self):
        """
        Prueba listar un almacen
        """
        self.registrar_almacen()
        self.registrar_almacen()

        respuesta = self.client.get("/almacenes")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)


    """
    ********************
    ******Secciones******
    ********************
    """

    def test_registrar_seccion(self):
        """
        Prueba el registro de una seccion
        """
        almacen = self.registrar_almacen()
        payload = {
            "nombre": "Mi seccion",
            "longitud": 1000,
            "altura": 1000,
            "anchura": 1000,
            "almacen": almacen.id
        }
        respuesta = self.client.post("/secciones", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)


    def test_modificar_seccion(self):
        """
        Prueba modificar una seccion
        """
        seccion = self.registrar_seccion()
        payload = {
            "nombre": "Mi seccion 2",
            "longitud": 1000,
            "altura": 1000,
            "anchura": 1000,
            "almacen": seccion.id
        }
        _id = str(seccion.id)
        respuesta = self.client.put("/secciones/" + _id, payload, format="json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], seccion.id)
        self.assertNotEqual(respuesta.json()["nombre"], seccion.nombre)

    def test_eliminar_seccion(self):
        """
        Prueba eliminar una seccion
        """
        seccion = self.registrar_seccion()
        _id = str(seccion.id)
        respuesta = self.client.delete("/secciones/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Seccion.objects.filter(id=seccion.id).first(), None)

    def test_buscar_seccion(self):
        """
        Prueba buscar una seccion
        """
        seccion = self.registrar_seccion()
        _id = str(seccion.id)
        respuesta = self.client.get("/secciones/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], seccion.id)

    def test_listar_seccion(self):
        """
        Prueba listar secciones
        """
        self.registrar_seccion()
        self.registrar_seccion()

        respuesta = self.client.get("/secciones")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)

    def test_registrar_seccion_volumen(self):
        """
        Prueba el registro de una seccion
        """
        almacen = self.registrar_almacen()
        payload = {
            "nombre": "Mi seccion",
            "longitud": 1000,
            "altura": 1000,
            "anchura": 1000,
            "almacen": almacen.id
        }
        respuesta = self.client.post("/secciones", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        volumen_esperado = payload["longitud"] * payload["anchura"] * payload["altura"]
        self.assertEqual(respuesta.json()["volumen"], volumen_esperado)
        self.assertEqual(respuesta.json()["volumen_restante"], volumen_esperado)

    """
    ********************
    ******Unidades******
    ********************
    """

    def test_registrar_unidad(self):
        """
        Prueba el registro de una unidad
        """
        compra = self.registrar_compra_con_detalles()
        detalle1 = compra.detalles.all()[0]
        seccion = self.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 1000,
            "altura": 1000,
            "ancho": 1000,
            "cantidad": 1
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

    def test_registrar_unidad_sobre_volumen(self):
        """
        Prueba el registro de una unidad con sobre volumen
        """
        compra = self.registrar_compra_con_detalles()
        detalle1 = compra.detalles.all()[0]
        seccion = self.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 1000,
            "altura": 1000,
            "ancho": 1100,
            "cantidad": 1
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json()["cantidad"], None)

    def test_registrar_unidad_sobre_volumen_cantidad(self):
        """
        Prueba el registro de una unidad con sobre volumen por cantidad
        """
        compra = self.registrar_compra_con_detalles()
        detalle1 = compra.detalles.all()[0]
        seccion = self.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 1000,
            "altura": 1000,
            "ancho": 800,
            "cantidad": 2
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json()["seccion"], None)

    def test_registrar_unidad_sobre_cantidad(self):
        """
        Prueba el registro de una unidad con sobre cantidad
        """
        compra = self.registrar_compra_con_detalles()
        detalle1 = compra.detalles.all()[0]
        seccion = self.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 2,
            "altura": 3,
            "ancho": 4,
            "cantidad": 20
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json()["cantidad"], None)

    def test_modificar_unidad(self):
        """
        Prueba modificar una unidad
        """
        unidad = self.registrar_unidad(1000, 1000, 1000)
        payload = {
            "unidad": unidad.unidad.id,
            "seccion": unidad.seccion.id,
            "longitud": 200,
            "altura": 1000,
            "ancho": 1000,
            "cantidad": 1
        }
        _id = str(unidad.id)
        respuesta = self.client.put("/unidades/" + _id, payload, format="json")
        self.assertEqual(respuesta.status_code, 200)

        self.assertEqual(respuesta.json()["id"], unidad.id)
        self.assertNotEqual(respuesta.json()["longitud"], unidad.longitud)

        volumen_esperado = payload["longitud"] * payload["ancho"] * payload["altura"]
        self.assertEqual(respuesta.json()["volumen"], volumen_esperado)

    def test_eliminar_unidad(self):
        """
        Prueba eliminar una unidad
        """
        unidad = self.registrar_unidad(1000, 1000, 1000)
        _id = str(unidad.id)
        respuesta = self.client.delete("/unidades/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Unidad.objects.filter(id=unidad.id).first(), None)

    def test_buscar_unidad(self):
        """
        Prueba buscar una unidad
        """
        unidad = self.registrar_unidad(1000, 1000, 1000)
        _id = str(unidad.id)
        respuesta = self.client.get("/unidades/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], unidad.id)

    def test_listar_unidad(self):
        """
        Prueba listar unidades
        """
        unidad = self.registrar_unidad(1000, 1000, 1000)
        unidad = self.registrar_unidad(1000, 1000, 1000, codigo="000013", categoria_nombre="otra")

        respuesta = self.client.get("/unidades")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)