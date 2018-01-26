from rest_framework import viewsets
from .models import Dependencia, Salida
from salidas import serializers
from rest_framework.exceptions import ValidationError
from personas.models import Persona

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.eliminable:
            error = {
                "salida": "no puede ser eliminada"
            }
            raise ValidationError(error)
        super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.eliminable:
            error = {
                "salida": "no puede ser modificada"
            }
            raise ValidationError(error)
        super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.persona)

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