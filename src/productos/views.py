from rest_framework import viewsets
from .models import Producto
from .models import Categoria
from .serializers import CategoriaSerializer
from .serializers import ProductoSerializer


class CategoriaVista(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoVista(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer