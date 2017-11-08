from .utils_casos_pruebas import UtilCasosPrueba
from productos.models import Producto

class CasosPruebas(UtilCasosPrueba):

    def test_registrar_producto(self):
        """
        Prueba el registro de un producto
        """
        payload = {
            "nombre": "Mi producto",
            "medida": Producto.KG,
            "categoria": self.registrar_categoria("mi categoria").id
        }
        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 201)

    def test_modificar_producto(self):
        """
        Prueba modificar  un producto
        """
        producto = Producto(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        payload = {
            "nombre": "Mi producto 2",
            "medida": Producto.KG,
            "categoria": self.registrar_categoria("mi categoria").id
        }
        _id = str(producto.id)
        respuesta = self.client.put("/productos/" + _id, payload)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], producto.id)
        self.assertNotEqual(respuesta.json()["nombre"], producto.nombre)

    def test_eliminar_producto(self):
        """
        Prueba eliminar un producto
        """
        producto = Producto(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        _id = str(producto.id)
        respuesta = self.client.delete("/productos/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Producto.objects.filter(id=producto.id).first(), None)

    def test_buscar_producto(self):
        """
        Prueba buscar un producto
        """
        producto = Producto(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        _id = str(producto.id)
        respuesta = self.client.get("/productos/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], producto.id)

    def test_registrar_producto_sin_campo(self):
        """
        Prueba el registro de un producto con datos faltantes
        """
        payload = {
            "medida": Producto.KG,
            "categoria": self.registrar_categoria("mi categoria").id
        }
        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 400)

    def test_registrar_producto_valor_erroneo(self):
        """
        Prueba el registro de un producto con datos erroneos
        """
        payload = {
            "model": "Producto 1",
            "medida": "ERROR",
            "categoria": self.registrar_categoria("mi categoria").id
        }
        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 400)