from productos.tests import UtilCasosPrueba

class CasosPruebas(UtilCasosPrueba):

    def test_registrar_productos(self):
        """
        Prueba el registro de un producto
        """
        payload = {
            "nombre": "Mi producto"
        }
        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 201)