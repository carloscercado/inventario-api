from rest_framework import viewsets
from .models import Cliente, Venta
from ventas import serializers


class VentaVista(viewsets.ModelViewSet):
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
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    #96609745