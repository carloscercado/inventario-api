from rest_framework import serializers
from .models import Proveedor, Compra

class ProveedorSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='proveedor-detail', format='html')
    class Meta:
        model = Proveedor
        fields = ("__all__")

class CompraSerializer(serializers.ModelSerializer):
    Proveedor = ProveedorSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='compra-detail', format='html')
    class Meta:
        model = Compra
        fields = ("__all__")
        #read_only_fields = ("cantidad",)

