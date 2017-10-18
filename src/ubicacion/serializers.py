from rest_framework import serializers
from .models import Almacen, Estante
from django.db import transaction

class AlmacenSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='almacen-detail', format='html')
    class Meta:
        model = Almacen
        fields = ("__all__")

class EstanteSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='estante-detail', format='html')
    class Meta:
        model = Estante
        fields = ("__all__")
        read_only_fields = ("capacidad_restante",)

    @transaction.atomic
    def create(self, data):
        plan = data.get("plan")
        estante = Estante(**data)
        estante.capacidad_restante = estante.capacidad_total
        estante.save()
        return estante

class AlmacenDetalleSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='almacen-detail', format='html')
    estantes = EstanteSerializer(many=True)
    class Meta:
        model = Almacen
        fields = ("nombre", "direccion", "telefono", "detalle",
                  "estantes")

