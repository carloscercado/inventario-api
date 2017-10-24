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
    medida = serializers.CharField(source='producto.medida')
    class Meta:
        model = DetalleCompra
        read_only_fields = ("total", "medida")
        fields = ("producto", "cantidad", "medida", "precio", "total", "cantidad_procesada",
                  "procesado", "faltante_por_procesar")

class CompraSerializer(serializers.ModelSerializer):
    Proveedor = ProveedorSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='compra-detail', format='html')
    class Meta:
        model = Compra
        fields = ("codigo", "total", "fecha", "detalle", "procesada",
                  "eliminable", "proveedor", "bloqueada",)
        read_only_fields = ("total",)

class CompraDetalleSerializer(CompraSerializer):
    detalles = DetalleCompraSerializer(many=True)
    class Meta(CompraSerializer.Meta):
        fields = ("codigo", "total", "fecha", "procesada", "eliminable",
                  "proveedor", "bloqueada","detalles",)

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        compra = Compra.objects.create(**datos)
        self.registrar_detalles(compra, detalles)
        return compra

    @transaction.atomic
    def update(self, compra, datos):
        detalles = datos.pop("detalles")
        for key, value in datos.items():
            setattr(compra, key, value)
        compra.borrar_detalles()
        self.registrar_detalles(compra, detalles)
        return compra

    def registrar_detalles(self, compra, detalles):
        registros = []
        compra.total = 0
        for i in detalles:
            detalle = DetalleCompra(**i, compra=compra,
                                    fecha=compra.fecha)
            compra.total = compra.total + detalle.total
            registros.append(detalle)
        compra.save()
        compra.detalles.bulk_create(registros)


