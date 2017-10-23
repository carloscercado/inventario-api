from rest_framework.exceptions import APIException

class InventarioError(APIException):
    status_code = 500
    default_detail = 'Plataforma fuera de servicio'
    default_code = 'problemas_con_plataforma'

    def __init__(self):
        self.detail = {
            "codigo": self.default_code,
            "mensaje": self.default_detail
        }
