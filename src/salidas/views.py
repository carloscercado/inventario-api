from rest_framework import viewsets
from .models import Cliente, Salida
from salidas import serializers


class SalidaVista(viewsets.ModelViewSet):
    """
    list: Lista todas las salidas
    create: Registra una salida
    retrieve: Busca una salida
    partial_update: Modifica parcialmente una salida  
    update: Modifica una salida
    delete: Elimina una salida
    """
    queryset = Salida.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SalidaListSerializer
        return serializers.SalidaSerializer

    def get_queryset(self):
        queryset = Salida.objects.all()\
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