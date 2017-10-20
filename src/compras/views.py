from rest_framework import viewsets
from .models import Proveedor
from .models import Compra
from .serializers import CompraSerializer
from .serializers import ProveedorSerializer


class CompraVista(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class ProveedorVista(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer