from .utils_casos_pruebas import UtilCasosPrueba
from ubicacion.models import Almacen, Seccion
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
                    "capacidad_total": 1000
                },
                {
                    "nombre": "mi estante 2",
                    "capacidad_total": 2000
                }
            ]
        }
        respuesta = self.client.post("/almacenes", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(len(respuesta.json().get("secciones")), 2)

    def test_modificar_almacen(self):
        """
        Prueba modificar  un almacen
        """
        almacen = self.registrar_almacen()
        payload = {
            "nombre": "Mi almacen 2",
            "direccion": "una direccion",
            "telefono": "02934164454",
            "secciones": []
        }
        _id = str(almacen.id)
        respuesta = self.client.put("/almacenes/" + _id, payload)
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
        respuesta = self.client.put("/secciones/" + _id, payload)
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
