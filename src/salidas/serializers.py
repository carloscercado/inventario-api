from rest_framework import serializers
from .models import Cliente, Salida, DetalleVenta
from django.db import transaction

class ClienteSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='cliente-detail', format='html')
    class Meta:
        model = Cliente
        fields = ("__all__")

class SalidaListSerializer(serializers.ModelSerializer):
    Cliente = ClienteSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='salida-detail', format='html')
    class Meta:
        model = Salida
        fields = ("__all__")
        read_only_fields = ("total",)

class DetalleSalidaSerializer(serializers.ModelSerializer):
    medida = serializers.CharField(source='producto.medida')
    class Meta:
        model = DetalleVenta
        fields = ("id", "cantidad", "medida", "producto")
        read_only_fields = ("id", "medida",)

class SalidaSerializer(SalidaListSerializer):
    detalles = DetalleSalidaSerializer(many=True)
    class Meta(SalidaListSerializer.Meta):
        model = Salida
        fields = ("cliente", "codigo", "fecha", "total", "detalles")

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        salida = Salida.objects.create(**datos)
        self.registrar_detalles(salida, detalles)
        return salida

    @transaction.atomic
    def update(self, salida, datos):
        detalles = datos.pop("detalles")
        for key, value in datos.items():
            setattr(salida, key, value)
        salida.borrar_detalles()
        self.registrar_detalles(salida, detalles)
        return salida

    def registrar_detalles(self, salida, detalles):
        registros = []
        salida.total = 0
        for i in detalles:
            detalle = DetalleVenta(**i, salida=salida,
                                   fecha=salida.fecha)
            #venta.total = venta.total + detalle.total
            registros.append(detalle)
        salida.save()
        salida.detalles.bulk_create(registros)



