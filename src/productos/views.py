from rest_framework import viewsets
from .models import Producto
from .models import Categoria
from productos import serializers


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

    def get_queryset(self):
        queryset = Producto.objects.all()\
                    .select_related("categoria")
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductoListSerializer
        return serializers.ProductoSerializer