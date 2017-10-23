from inventario.exceptions import InventarioError

class CantidadInvalidadError(InventarioError):
    status_code = 400
    default_detail = 'cantidad es mayor a la disponible por procesar'
    default_code = 'cantidad_invalida'

    def __init__(self):
        super().__init__()

class ProductoProcesadoError(InventarioError):
    status_code = 400
    default_detail = 'producto ya esta procesado'
    default_code = 'producto_invalido'

    def __init__(self):
        super().__init__()