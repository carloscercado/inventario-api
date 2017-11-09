from .utils_casos_pruebas import UtilCasosPrueba
from ubicacion.models import Almacen
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
            "estantes": []
        }
        respuesta = self.client.post("/almacenes", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

    def test_registrar_almacen_con_estantes(self):
        """
        Prueba el registro de un almacen cin estantes
        """
        payload = {
            "nombre": "Mi almacen",
            "direccion": "mi direccion",
            "telefono": "02934333333",
            "estantes": [
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
        self.assertEqual(len(respuesta.json().get("estantes")), 2)

    def test_modificar_almacen(self):
        """
        Prueba modificar  un almacen
        """
        almacen = Almacen(nombre="mi almacen", direccion="mi direccion",
                          telefono="02924333323")
        almacen.save()
        payload = {
            "nombre": "Mi almacen 2",
            "direccion": "una direccion",
            "telefono": "02934164454",
            "estantes": []
        }
        _id = str(almacen.id)
        respuesta = self.client.put("/almacenes/" + _id, payload)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], almacen.id)
        self.assertNotEqual(respuesta.json()["nombre"], almacen.nombre)

    def test_eliminar_Almacen(self):
        """
        Prueba eliminar un producto
        """
        producto = Almacen(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        _id = str(producto.id)
        respuesta = self.client.delete("/productos/" + _id)
        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(Producto.objects.filter(id=producto.id).first(), None)

    def test_buscar_Almacen(self):
        """
        Prueba buscar un producto
        """
        producto = Almacen(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        _id = str(producto.id)
        respuesta = self.client.get("/productos/" + _id)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["id"], producto.id)

    def test_listar_Almacen(self):
        """
        Prueba listar un producto
        """
        producto = Almacen(nombre="Mi producto", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria"))
        producto.save()
        producto = Almacen(nombre="Mi producto 2", medida=Producto.KG,
                            categoria=self.registrar_categoria("mi categoria 2"))
        producto.save()
        respuesta = self.client.get("/productos")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 2)