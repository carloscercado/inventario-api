from rest_framework import serializers
from .models import Proveedor, Compra, DetalleCompra
from django.db import transaction

class ProveedorSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='proveedor-detail', format='html')
    class Meta:
        model = Proveedor
        fields = ("__all__")
        read_only_fields = ("ultimo_pedido",)

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ("__all__")
        read_only_fields = ("compra", )

class CompraSerializer(serializers.ModelSerializer):
    Proveedor = ProveedorSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='compra-detail', format='html')
    class Meta:
        model = Compra
        fields = ("__all__")
        read_only_fields = ("total",)

class CompraDetalleSerializer(CompraSerializer):
    detalles = DetalleCompraSerializer(many=True)
    class Meta(CompraSerializer.Meta):
        pass

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        registros = []
        compra = Compra.objects.create(**datos)
        for i in detalles:
            detalle = DetalleCompra(**i, compra=compra)
            producto = detalle.producto
            cantidad = producto.cantidad_transito
            producto.cantidad_transito = cantidad + i.get("cantidad")
            producto.save()
            registros.append(detalle)
        compra.detalles.bulk_create(registros)
        return compra


