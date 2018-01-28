from rest_framework import serializers
from .models import Categoria, Producto
import uuid

class CategoriaSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='categoria-detail', format='html')
    class Meta:
        model = Categoria
        fields = ("id", "nombre","eliminable", "detalle", "codigo")
        read_only_fields = ("codigo",)

    def create(self, datos):
        categoria = Categoria.objects.create(**datos, codigo=uuid.uuid4().hex)
        return categoria

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ("__all__")
        read_only_fields = ("cantidad", "codigo",)

    def create(self, datos):
        producto = Producto.objects.create(**datos, codigo=uuid.uuid4().hex)
        producto.categoria.eliminable = False
        producto.categoria.save()
        return producto

class ProductoListSerializer(ProductoSerializer):
    categoria = CategoriaSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='producto-detail', format='html')
    class Meta(ProductoSerializer.Meta):
        pass
