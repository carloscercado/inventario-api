from rest_framework import viewsets
from .models import Producto
from .models import Categoria
from productos import serializers
from rest_framework.response import Response
from productos.exceptions import CategoriaNoEliminable


class CategoriaVista(viewsets.ModelViewSet):
    """
    list: Lista todas las categorias
    create: Registra una categoria
    retrieve: Busca una categoria
    partial_update: Modifica parcialmente una categoria
    update: Modifica una categoria
    delete: Elimina una categoria
    """
    queryset = Categoria.objects.all()
    serializer_class = serializers.CategoriaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.eliminable:
            raise CategoriaNoEliminable()
        self.perform_destroy(instance)
        if instance.productos.all().first() is None:
            instance.eliminable = True
            instance.save()
        return Response(status=204)

class ProductoVista(viewsets.ModelViewSet):
    """
    list: Lista todos los productos
    create: Registra un producto
    retrieve: Busca un producto
    partial_update: Modifica parcialmente el producto
    update: Modifica un producto
    delete: Elimina un producto
    """
    queryset = Producto.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        categoria = instance.categoria
        self.perform_destroy(instance)
        if categoria.productos.all().first() is None:
            categoria.eliminable = True
            categoria.save()
        return Response(status=204)

    def get_queryset(self):
        queryset = Producto.objects.all()\
                    .select_related("categoria")
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductoListSerializer
        return serializers.ProductoSerializer