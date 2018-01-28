from rest_framework import serializers
from .models import Proveedor, Compra, DetalleCompra
from django.db import transaction
from rest_framework.exceptions import ValidationError
import uuid

class ProveedorSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='proveedor-detail', format='html')
    rif = serializers.RegexField(r'^[JGVE][-][0-9]{8}[-][0-9]$', max_length=12, min_length=11)
    telefono = serializers.RegexField(r'[0-9]{3}[-][0-9]{7}$', max_length=11, min_length=11)
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

class DetalleCompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        read_only_fields = ("total",)
        fields = ("producto", "cantidad", "precio", "total", "cantidad_procesada",
                  "procesado", "faltante_por_procesar")

class CompraSerializer(serializers.ModelSerializer):
    Proveedor = ProveedorSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='compra-detail', format='html')
    class Meta:
        model = Compra
        fields = ("id","codigo", "total", "fecha", "detalle", "procesada",
                  "eliminable", "proveedor", "bloqueada",)
        read_only_fields = ("total","codigo")

class CompraDetalleSerializer(CompraSerializer):
    detalles = DetalleCompraCreateSerializer(many=True)
    class Meta(CompraSerializer.Meta):
        fields = ("id","codigo", "total", "fecha", "procesada", "eliminable",
                  "proveedor", "bloqueada","detalles",)

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        codigo = uuid.uuid4().hex
        compra = Compra.objects.create(**datos, codigo=codigo)
        self.registrar_detalles(compra, detalles)
        return compra

    @transaction.atomic
    def update(self, compra, datos):
        if compra.bloqueada:
            error = {
                "compra": "no puede ser modificada, esta bloqueada"
            }
            raise ValidationError(error)
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


