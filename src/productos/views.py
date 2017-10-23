from rest_framework import viewsets
from .models import Producto
from .models import Categoria
from productos import serializers


class CategoriaVista(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = serializers.CategoriaSerializer

class ProductoVista(viewsets.ModelViewSet):
    queryset = Producto.objects.all()

    def get_queryset(self):
        queryset = Producto.objects.all()\
                    .select_related("categoria")
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductoListSerializer
        return serializers.ProductoSerializer