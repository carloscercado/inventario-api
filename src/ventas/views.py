from rest_framework import viewsets
from .models import Cliente
from .models import Venta
from .serializers import VentaSerializer
from .serializers import ClienteSerializer


class VentaVista(viewsets.ModelViewSet):
    """
    list: Lista todas las ventas
    create: Registra una venta
    retrieve: Busca una venta
    partial_update: Modifica parcialmente una venta  
    update: Modifica una venta
    delete: Elimina una venta
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class ClienteVista(viewsets.ModelViewSet):
    """
    list: Lista todos los clientes
    create: Registra un cliente
    retrieve: Busca un cliente
    partial_update: Modifica parcialmente un cliente  
    update: Modifica un cliente
    delete: Elimina un cliente
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer