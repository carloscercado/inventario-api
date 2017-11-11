from rest_framework import viewsets
from .models import Seccion, Almacen, Unidad
from ubicacion import serializers


class AlmacenVista(viewsets.ModelViewSet):
    """
    list: Lista todos los almacenes
    create: Registra una almacen
    retrieve: Busca una almacen
    partial_update: Modifica parcialmente una almacen
    update: Modifica una almacen
    delete: Elimina una almacen
    """
    queryset = Almacen.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AlmacenSerializer
        return serializers.AlmacenDetalleSerializer

class SeccionVista(viewsets.ModelViewSet):
    """
    list: Lista todos las secciones
    create: Registra un seccion
    retrieve: Busca un seccion
    partial_update: Modifica parcialmente un seccion
    update: Modifica un seccion
    delete: Elimina un seccion
    """
    queryset = Seccion.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.SeccionAlmacenSerializer
        return serializers.SeccionSerializer


class UnidadVista(viewsets.ModelViewSet):
    """
    list: Lista todas las unidades
    create: Registra una unidad
    retrieve: Busca una unidad
    partial_update: Modifica parcialmente una unidad
    update: Modifica una unidad
    delete: Elimina una unidad
    """
    queryset = Unidad.objects.all()
    serializer_class = serializers.UnidadSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UnidadListSerializer
        return serializers.UnidadSerializer

    def get_queryset(self):
        queryset = Unidad.objects.all()\
                    .select_related("unidad", "seccion")
        return queryset
