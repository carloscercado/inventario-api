from rest_framework import viewsets
from .models import Cliente
from .models import Venta
from .serializers import VentaSerializer
from .serializers import ClienteSerializer


class VentaVista(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class ClienteVista(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer