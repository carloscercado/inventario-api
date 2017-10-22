from rest_framework import viewsets
from .models import Proveedor
from .models import Compra
from compras import serializers


class CompraVista(viewsets.ModelViewSet):
    queryset = Compra.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CompraSerializer
        return serializers.CompraDetalleSerializer

    def get_queryset(self):
        queryset = Compra.objects.all()\
                    .select_related("proveedor")\
                    .prefetch_related("detalles")
        return queryset

class ProveedorVista(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = serializers.ProveedorSerializer