from rest_framework import viewsets
from .models import Dependencia, Salida
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
                    .select_related("dependencia")\
                    .prefetch_related("detalles")
        return queryset

class DependenciaVista(viewsets.ModelViewSet):
    """
    list: Lista todos las dependencias
    create: Registra una dependencia
    retrieve: Busca una dependencia
    partial_update: Modifica parcialmente una dependencia  
    update: Modifica una dependencia
    delete: Elimina una dependencia
    """
    queryset = Dependencia.objects.all()
    serializer_class = serializers.DependenciaSerializer

    #96609745