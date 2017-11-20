from rest_framework import serializers
from .models import Dependencia, Salida, DetalleSalida
from django.db import transaction
import uuid
from rest_framework.exceptions import ValidationError



class DependenciaSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='dependencia-detail', format='html')
    class Meta:
        model = Dependencia
        fields = ("__all__")

class SalidaListSerializer(serializers.ModelSerializer):
    Dependencia = DependenciaSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='salida-detail', format='html')
    class Meta:
        model = Salida
        fields = ("__all__")
        read_only_fields = ("total",)

class DetalleSalidaSerializer(serializers.ModelSerializer):

    def validate(self, values):
        producto = values.get("producto")
        cantidad = values.get("cantidad")

        if producto.cantidad == 0:
            error = {
                "producto": "esta escaso, no hay cantidad disponible"
            }
            raise ValidationError(error)

        if producto.cantidad < cantidad:
            error = {
                "cantidad": "incorrecta, es mayor a la cantidad disponible ["+str(producto.cantidad)+"]"
            }
            raise ValidationError(error)
        return values

    class Meta:
        model = DetalleSalida
        fields = ("id", "cantidad", "producto", "fecha",)
        read_only_fields = ("id", "fecha",)

class SalidaSerializer(SalidaListSerializer):
    detalles = DetalleSalidaSerializer(many=True)
    class Meta(SalidaListSerializer.Meta):
        model = Salida
        fields = ("dependencia", "codigo", "fecha", "total", "detalles")
        read_only_fields = ("codigo",)

    @transaction.atomic
    def create(self, datos):
        detalles = datos.pop("detalles")
        codigo = uuid.uuid4().hex
        salida = Salida.objects.create(**datos, codigo=codigo)
        self.registrar_detalles(salida, detalles)
        return salida

    @transaction.atomic
    def update(self, salida, datos):
        detalles = datos.pop("detalles")
        for key, value in datos.items():
            setattr(salida, key, value)
        return salida

    def registrar_detalles(self, salida, detalles):
        registros = []
        salida.total = 0
        for i in detalles:
            detalle = DetalleSalida(**i, salida=salida,
                                   fecha=salida.fecha)
            #venta.total = venta.total + detalle.total
            registros.append(detalle)
        salida.save()
        salida.detalles.bulk_create(registros)
        salida.aplicar_metodo_fifo()



