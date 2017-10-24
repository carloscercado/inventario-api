from rest_framework import serializers
from .models import Cliente, Venta, DetalleVenta
from django.db import transaction

class ClienteSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='cliente-detail', format='html')
    class Meta:
        model = Cliente
        fields = ("__all__")

class VentaListSerializer(serializers.ModelSerializer):
    Cliente = ClienteSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='venta-detail', format='html')
    class Meta:
        model = Venta
        fields = ("__all__")
        read_only_fields = ("total",)

class DetalleVentaSerializer(serializers.ModelSerializer):
    medida = serializers.CharField(source='producto.medida')
    class Meta:
        model = DetalleVenta
        fields = ("id", "cantidad", "medida", "producto")
        read_only_fields = ("id", "medida",)

class VentaSerializer(VentaListSerializer):
    detalles = DetalleVentaSerializer(many=True)
    class Meta(VentaListSerializer.Meta):
        model = Venta
        fields = ("cliente", "codigo", "fecha", "total", "detalles")

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        venta = Venta.objects.create(**datos)
        self.registrar_detalles(venta, detalles)
        return venta

    @transaction.atomic
    def update(self, venta, datos):
        detalles = datos.pop("detalles")
        for key, value in datos.items():
            setattr(venta, key, value)
        venta.borrar_detalles()
        self.registrar_detalles(venta, detalles)
        return venta

    def registrar_detalles(self, venta, detalles):
        registros = []
        venta.total = 0
        for i in detalles:
            detalle = DetalleVenta(**i, venta=venta,
                                   fecha=venta.fecha)
            #venta.total = venta.total + detalle.total
            registros.append(detalle)
        venta.save()
        venta.detalles.bulk_create(registros)



