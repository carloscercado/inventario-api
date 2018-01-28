from .utils_casos_pruebas import UtilCasosPrueba
from compras.models import Proveedor, Compra
import uuid
from ubicacion.tests import utils_casos_pruebas
import productos
import pdb

class CasosPruebas(UtilCasosPrueba):

    """
    ********************
    ******Compras******
    ********************
    """

    def test_registrar_proveedor(self):
        """
        Prueba el registro de un proveedor
        """
        payload = {
            "nombre": "Mi proveedor",
            "direccion": "mi direccion",
            "rif": "V-23923164-1",
            "telefono": "293-1447264"
        }
        respuesta = self.client.post("/proveedores", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

    def test_registrar_proveedor_rif_y_telefono_incorrecto(self):
        """
        Prueba el registro de un proveedor con formato de rif incorrecto
        """
        payload = {
            "nombre": "Mi proveedor",
            "direccion": "mi direccion",
            "rif": "23923164",
            "telefono": "0293-1447264"
        }
        respuesta = self.client.post("/proveedores", payload, format="json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json().get("rif"), None)
        self.assertNotEqual(respuesta.json().get("telefono"), None)

    def test_modificar_proveedor(self):
        """
        Prueba modificar un proveedor
        """
        proveedor = self.registrar_proveedor()
        payload = {
            "nombre": "Mi proveedor",
            "direccion": "mi direccion",
            "rif": "V-23923164-1",
            "telefono": "293-1447264"
        }
        _id = str(proveedor.id)
        respuesta = self.client.put("/proveedores/" + _id, payload, format="json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], proveedor.id)
        self.assertNotEqual(respuesta.json()["nombre"], proveedor.nombre)

    def test_eliminar_proveedor(self):
        """
        Prueba eliminar un proveedor
        """
        proveedor = self.registrar_proveedor()
        _id = str(proveedor.id)
        respuesta = self.client.delete("/proveedores/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Proveedor.objects.filter(id=proveedor.id).first(), None)

    def test_buscar_proveedor(self):
        """
        Prueba buscar un proveedor
        """
        proveedor = self.registrar_proveedor()
        _id = str(proveedor.id)
        respuesta = self.client.get("/proveedores/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], proveedor.id)

    def test_listar_proveedor(self):
        """
        Prueba listar proveedores
        """
        self.registrar_proveedor()
        self.registrar_proveedor()

        respuesta = self.client.get("/proveedores")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)



    def test_registrar_compra_vacia(self):
        """
        Prueba el registro de una compra vacia
        """

        proveedor = self.registrar_proveedor()
        payload = {
            "fecha": "2017-01-02",
            "proveedor": proveedor.id,
            "detalles": []
        }
        respuesta = self.client.post("/compras", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(len(respuesta.json().get("codigo")), 32)

    def test_registrar_compra(self):
        """
        Prueba el registro de una compra
        """

        proveedor = self.registrar_proveedor()
        producto = self.registrar_producto()

        payload = {
            "fecha": "2017-01-02",
            "proveedor": proveedor.id,
            "detalles": [
                {
                    "producto": producto.id,
                    "precio": 1000,
                    "cantidad": 5
                }
            ]
        }
        respuesta = self.client.post("/compras", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json().get("bloqueada"), False)
        self.assertEqual(respuesta.json().get("procesada"), False)
        self.assertEqual(respuesta.json().get("eliminable"), True)


    def test_modificar_compra(self):
        """
        Prueba modificar una compra
        """
        compra = self.registrar_compra()
        self.assertEqual(len(compra.detalles.all()), 0)

        producto = self.registrar_producto()
        payload = {
            "fecha": "2017-01-02",
            "proveedor": compra.proveedor.id,
            "detalles": [
                {
                    "producto": producto.id,
                    "precio": 1000,
                    "cantidad": 5
                },
                {
                    "producto": producto.id,
                    "precio": 500,
                    "cantidad": 5
                }
            ]
        }
        _id = str(compra.id)

        respuesta = self.client.post("/compras", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(len(respuesta.json()["detalles"]), 2)

    def test_eliminar_compra(self):
        """
        Prueba eliminar una compra
        """
        compra = self.registrar_compra_con_detalles()
        _id = str(compra.id)
        respuesta = self.client.delete("/compras/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Compra.objects.filter(id=compra.id).first(), None)

    def test_buscar_compra(self):
        """
        Prueba buscar un compra
        """
        compra = self.registrar_compra_con_detalles()
        _id = str(compra.id)
        respuesta = self.client.get("/compras/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], compra.id)
        self.assertEqual(len(respuesta.json().get("detalles")), 2)

    def test_listar_compra(self):
        """
        Prueba listar compras
        """
        self.registrar_compra_con_detalles(codigo="0000001", categoria_nombre="Otra categoria")
        self.registrar_compra_con_detalles(codigo="0000002")

        respuesta = self.client.get("/compras")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)

    def test_procesar_compra(self):
        """
        Prueba el procesamiento de una compra
        """

        compra = self.registrar_compra_con_detalles(categoria_nombre="Otra categoria")
        detalle1 = compra.detalles.all().first()
        detalle2 = compra.detalles.all().last()
        _id = str(detalle1.producto.id)
        clase = utils_casos_pruebas.UtilCasosPrueba()
        seccion = clase.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 200,
            "altura": 200,
            "ancho": 200,
            "cantidad": detalle1.cantidad
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        payload = {
            "unidad": detalle2.id,
            "seccion": seccion.id,
            "longitud": 200,
            "altura": 200,
            "ancho": 200,
            "cantidad": detalle2.cantidad
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)


        compra_id = str(compra.id)

        respuesta = self.client.get("/compras/" + compra_id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json().get("bloqueada"), True)
        self.assertEqual(respuesta.json().get("procesada"), True)
        self.assertEqual(respuesta.json().get("eliminable"), False)

    def test_bloquear_compra(self):
        """
        Prueba si se bloquea una compra cuando debe
        """

        compra = self.registrar_compra_con_detalles(categoria_nombre="Otra categoria")
        detalle1 = compra.detalles.all().first()
        _id = str(detalle1.producto.id)
        clase = utils_casos_pruebas.UtilCasosPrueba()
        seccion = clase.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 200,
            "altura": 200,
            "ancho": 200,
            "cantidad": detalle1.cantidad
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        compra_id = str(compra.id)

        respuesta = self.client.get("/compras/" + compra_id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json().get("bloqueada"), True)

    def test_eliminar_compra_bloqueada(self):
        """
        Prueba eliminar una compra bloqueada
        """

        compra = self.registrar_compra_con_detalles(categoria_nombre="Otra categoria")
        detalle1 = compra.detalles.all().first()
        _id = str(detalle1.producto.id)
        clase = utils_casos_pruebas.UtilCasosPrueba()
        seccion = clase.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 200,
            "altura": 200,
            "ancho": 200,
            "cantidad": detalle1.cantidad
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        compra_id = str(compra.id)

        respuesta = self.client.delete("/compras/" + compra_id)
        self.assertEqual(respuesta.status_code, 400)

    def test_modificar_compra_bloqueada(self):
        """
        Prueba modificar una compra bloqueada
        """

        compra = self.registrar_compra_con_detalles(categoria_nombre="Otra categoria")
        detalle1 = compra.detalles.all().first()
        _id = str(detalle1.producto.id)
        clase = utils_casos_pruebas.UtilCasosPrueba()
        seccion = clase.registrar_seccion()
        payload = {
            "unidad": detalle1.id,
            "seccion": seccion.id,
            "longitud": 200,
            "altura": 200,
            "ancho": 200,
            "cantidad": detalle1.cantidad
        }
        respuesta = self.client.post("/unidades", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        compra_id = str(compra.id)

        payload = {
            "fecha": "2017-01-02",
            "proveedor": compra.proveedor.id,
            "detalles": []
        }

        respuesta = self.client.put("/compras/" + compra_id, payload, format="json")
        self.assertEqual(respuesta.status_code, 400)

