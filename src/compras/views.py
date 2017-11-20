from rest_framework import viewsets
from rest_framework.decorators import list_route
from .models import Proveedor, Compra, DetalleCompra
from compras import serializers
from personas.models import Persona
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class CompraVista(viewsets.ModelViewSet):
    """
    list: Lista todas las compras
    create: Registra una compra
    retrieve: Busca una compra
    partial_update: Modifica parcialmente una compra
    update: Modifica una compra
    delete: Elimina una compra
    """
    queryset = Compra.objects.all()


    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        compra = self.get_queryset().filter(id=pk).get()
        if not compra.eliminable:
            error = {
                "compra": "no puede ser eliminada, esta bloqueada"
            }
            raise ValidationError(error)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CompraSerializer
        return serializers.CompraDetalleSerializer

    def get_queryset(self):
        queryset = Compra.objects.all()\
                    .select_related("proveedor")\
                    .prefetch_related("detalles")
        return queryset

    def perform_create(self, serializer):
        serializer_class = serializers.CompraDetalleSerializer
        user = Persona.objects.filter(user=self.request.user).get()
        serializer.save(usuario=user)

    @list_route(methods=['get'], url_path=r'codigo/(?P<codigo>[^/]+)')
    def por_plan_de_cuenta(self, request, codigo):
        data = self.get_queryset().filter(codigo=codigo).first()
        serializer = serializers.DetalleCompraSerializer(data.detalles, many=True,
                                                       context={'request': request})
        return Response(serializer.data)


class ProveedorVista(viewsets.ModelViewSet):
    """
    list: Lista todos los proveedores
    create: Registra un proveedor
    retrieve: Busca un proveedor
    partial_update: Modifica parcialmente un proveedor
    update: Modifica un proveedor
    delete: Elimina un proveedor
    """
    queryset = Proveedor.objects.all()
    serializer_class = serializers.ProveedorSerializer