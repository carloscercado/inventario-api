from rest_framework import viewsets
from rest_framework.decorators import list_route
from .models import Proveedor, Compra, DetalleCompra
from compras import serializers
from rest_framework.response import Response


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

    @list_route(methods=['get'], url_path=r'codigo/(?P<codigo>[^/]+)')
    def por_plan_de_cuenta(self, request, codigo):
        data = self.get_queryset().filter(codigo=codigo).first()
        serializer = serializers.DetalleCompraSerializer(data.detalles, many=True,
                                                       context={'request': request})
        return Response(serializer.data)


class ProveedorVista(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = serializers.ProveedorSerializer