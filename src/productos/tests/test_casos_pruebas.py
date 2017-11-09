from .utils_casos_pruebas import UtilCasosPrueba
from productos.models import Producto, Categoria
import pdb

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
        categoria = self.registrar_categoria("mi categoria")
        producto = Producto(nombre="Mi producto", medida=Producto.KG,
                            categoria=categoria)
        producto.save()
        payload = {
            "nombre": "Mi producto 2",
            "medida": Producto.KG,
            "categoria": categoria.id
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

    def test_listar_producto(self):
        """
        Prueba listar un producto
        """
        producto = Producto(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        producto = Producto(nombre="Mi producto 2", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria 2"))
        producto.save()
        respuesta = self.client.get("/productos")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)

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

    def test_registrar_producto_falla_integridad_dominio(self):
        """
        Prueba el registro de un producto con datos fallos
        """
        payload = {
            "nombre": "Mi producto con una descripcion muy pero muy larga",
            "medida": Producto.KG,
            "categoria": self.registrar_categoria("mi categoria").id
        }
        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json().get("nombre"), None)








    def test_registrar_categoria(self):
        """
        Prueba el registro de una categoria
        """
        payload = {
            "nombre": "Mi Categoria"
        }
        respuesta = self.client.post("/categorias", payload)
        self.assertEqual(respuesta.status_code, 201)

    def test_modificar_categoria(self):
        """
        Prueba modificar una categoria
        """
        categoria = self.registrar_categoria("mi categoria")
        payload = {
            "nombre": "Mi categoria 2"
        }
        _id = str(categoria.id)
        respuesta = self.client.put("/categorias/" + _id, payload)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], categoria.id)
        self.assertNotEqual(respuesta.json()["nombre"], categoria.nombre)

    def test_buscar_categoria(self):
        """
        Prueba buscar una categoria
        """
        categoria = self.registrar_categoria("mi categoria")
        _id = str(categoria.id)
        respuesta = self.client.get("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], categoria.id)

    def test_eliminar_categoria(self):
        """
        Prueba eliminar una categoria
        """
        categoria = self.registrar_categoria("mi categoria")
        _id = str(categoria.id)
        respuesta = self.client.delete("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Categoria.objects.filter(id=categoria.id).first(), None)

    def test_listar_categoria(self):
        """
        Prueba listar categorias
        """
        categoria = self.registrar_categoria("mi categoria")
        categoria = self.registrar_categoria("mi categoria 2")

        respuesta = self.client.get("/categorias")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)

    def test_registrar_categoria_integridad_dominio(self):
        """
        Prueba el registro de una categoria con datos fallos
        """
        payload = {
            "nombre": "Mi Categoria con un nombre, o descripcion muy grande"
        }
        respuesta = self.client.post("/categorias", payload)
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json().get("nombre"), None)

    def test_registrar_categoria_integridad_nombre(self):
        """
        Prueba el registro de una categoria con fallos integridad nombre
        """
        categoria = self.registrar_categoria("mi categoria")
        payload = {
            "nombre": "mi categoria"
        }
        respuesta = self.client.post("/categorias", payload)
        self.assertEqual(respuesta.status_code, 400)
        self.assertNotEqual(respuesta.json().get("nombre"), None)

    def test_eliminar_categoria_usada(self):
        """
        Prueba eliminar una categoria usada
        """
        producto = self.registrar_producto()
        _id = str(producto.categoria.id)
        respuesta = self.client.delete("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 400)

    def test_eliminar_categoria_usada_varias(self):
        """
        Prueba eliminar una categoria usada varias
        """
        producto = self.registrar_producto()
        producto2 = self.registrar_producto(categoria_nombre="Mi otra categoria")
        producto2.categoria = producto.categoria
        producto2.save()

        _id = str(producto.categoria.id)
        respuesta = self.client.delete("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 400)

        _id_producto = str(producto.id)
        respuesta = self.client.delete("/productos/" + _id_producto)
        self.assertEqual(respuesta.status_code, 204)

        respuesta = self.client.delete("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 400)

        _id_producto2 = str(producto2.id)
        respuesta = self.client.delete("/productos/" + _id_producto2)
        self.assertEqual(respuesta.status_code, 204)

        respuesta = self.client.delete("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 204)

    def test_cambio_estado_categoria(self):
        """
        Prueba el cambio de estado de una categoria
        """
        categoria = self.registrar_categoria("mi categoria")
        _id = str(categoria.id)
        payload = {
            "nombre": "Mi producto",
            "medida": Producto.KG,
            "categoria": _id
        }

        self.assertEqual(categoria.eliminable, True)

        respuesta = self.client.post("/productos", payload)
        self.assertEqual(respuesta.status_code, 201)

        respuesta = self.client.get("/categorias/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["eliminable"], False)
