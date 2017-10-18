from rest_framework import viewsets
from .models import Estante
from .models import Almacen
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