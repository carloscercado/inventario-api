from rest_framework import viewsets
from .models import Cliente, Venta
from ventas import serializers


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

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VentaListSerializer
        return serializers.VentaSerializer

    def get_queryset(self):
        queryset = Venta.objects.all()\
                    .select_related("cliente")\
                    .prefetch_related("detalles")
        return queryset

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
    serializer_class = serializers.ClienteSerializer

    #96609745