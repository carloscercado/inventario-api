from rest_framework import viewsets
from .models import Estante, Almacen, Unidad
from ubicacion import serializers


class AlmacenVista(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AlmacenSerializer
        return serializers.AlmacenDetalleSerializer

class EstanteVista(viewsets.ModelViewSet):
    queryset = Estante.objects.all()
    serializer_class = serializers.EstanteSerializer

class UnidadVista(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = serializers.UnidadSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UnidadListSerializer
        return serializers.UnidadSerializer

    def get_queryset(self):
        queryset = Unidad.objects.all()\
                    .select_related("unidad", "estante")
        return queryset
