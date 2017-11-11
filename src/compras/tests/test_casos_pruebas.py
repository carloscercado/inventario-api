from .utils_casos_pruebas import UtilCasosPrueba
from compras.models import Proveedor, Compra
import uuid
import productos
import pdb

class CasosPruebas(UtilCasosPrueba):

    """
    ********************
    ******Proveedores******
    ********************
    """

    def test_registrar_proveedor(self):
        """
        Prueba el registro de un proveedor
        """
        payload = {
            "nombre": "Mi proveedor",
            "direccion": "mi direccion",
            "rif": "23923164",
            "telefono": "0293144726"
        }
        respuesta = self.client.post("/proveedores", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)


    def test_modificar_proveedor(self):
        """
        Prueba modificar un proveedor
        """
        proveedor = self.registrar_proveedor()
        payload = {
            "nombre": "Mi proveedor 2",
            "direccion": "mi direccion",
            "rif": "23923164",
            "telefono": "0293144726"
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

    """
    ********************
    ******Compras******
    ********************
    """

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

    """
    probar procesar compra
    probar bloquear una compra
    probar eliminar/modificar compra bloqueada
    """