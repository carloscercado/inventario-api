from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='categoria-detail', format='html')
    class Meta:
        model = Categoria
        fields = ("nombre","detalle")

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='producto-detail', format='html')
    class Meta:
        model = Producto
        fields = ("nombre", "categoria","detalle", "cantidad", "medida", "minimo",)
        read_only_fields = ("cantidad",)

