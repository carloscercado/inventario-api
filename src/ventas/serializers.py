from rest_framework import serializers
from .models import Cliente, Venta

class ClienteSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='cliente-detail', format='html')
    class Meta:
        model = Cliente
        fields = ("__all__")

class VentaSerializer(serializers.ModelSerializer):
    Cliente = ClienteSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='venta-detail', format='html')
    class Meta:
        model = Venta
        fields = ("__all__")
        #read_only_fields = ("cantidad",)

