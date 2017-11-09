from rest_framework.exceptions import APIException

class InventarioException(APIException):
    status_code = 500
    default_detail = 'Error de plataforma'
    default_code = 'service_unavailable'

class CategoriaNoEliminable(InventarioException):
    status_code = 400
    default_detail = 'Categoria no puede ser eliminada'
    default_code = 'categoria_bloqueada'