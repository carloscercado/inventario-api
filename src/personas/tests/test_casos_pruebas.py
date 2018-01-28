from .utils_casos_pruebas import UtilCasosPrueba
from productos.models import Producto, Categoria
from ubicacion.tests import utils_casos_pruebas
import uuid
class CasosPruebas(UtilCasosPrueba):

    """
    ********************
    ******Personas******
    ********************
    """

    def test_registrar_persona(self):
        """
        Prueba el registro de un persona
        """
        payload = {
            "nombre": "Mi producto",


        }