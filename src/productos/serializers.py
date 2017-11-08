from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='categoria-detail', format='html')
    class Meta:
        model = Categoria
        fields = ("nombre","detalle")

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ("__all__")
        read_only_fields = ("cantidad",)

class ProductoListSerializer(ProductoSerializer):
    categoria = CategoriaSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='producto-detail', format='html')
    class Meta(ProductoSerializer.Meta):
        pass
