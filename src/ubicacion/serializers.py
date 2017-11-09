from rest_framework import serializers
from .models import Almacen, Estante, Unidad
from django.db import transaction
from .exceptions import CantidadInvalidadError, ProductoProcesadoError
import uuid

class AlmacenSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='almacen-detail', format='html')
    class Meta:
        model = Almacen
        fields = ("__all__")
        read_only_fields = ("eliminable", )

class EstanteSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='estante-detail', format='html')
    class Meta:
        model = Estante
        fields = ("nombre", "capacidad_total", "capacidad_restante", "detalle")
        read_only_fields = ("capacidad_restante",)

    @transaction.atomic
    def create(self, data):
        plan = data.get("plan")
        estante = Estante(**data)
        estante.capacidad_restante = estante.capacidad_total
        estante.save()
        return estante

class AlmacenDetalleSerializer(serializers.ModelSerializer):
    estantes = EstanteSerializer(many=True)
    class Meta:
        model = Almacen
        fields = ("id", "nombre", "direccion", "telefono", "estantes")
        #read_only_fields = ("eliminable", "estantes", "detalle")

    @transaction.atomic
    def create(self, datos):
        estantes = datos.pop("estantes")
        almacen = Almacen.objects.create(**datos)
        self.registrar_estantes(almacen, estantes)
        return almacen

    @transaction.atomic
    def update(self, almacen, datos):
        estantes = datos.pop("estantes")
        for key, value in datos.items():
            setattr(almacen, key, value)
        #almacen.borrar_estantes()
        #self.registrar_estantes(almacen, estantes)
        return almacen

    def registrar_estantes(self, almacen, estantes):
        registros = []
        for i in estantes:
            estante = Estante(**i, almacen=almacen,
                              capacidad_restante=i.get("capacidad_total"))
            registros.append(estante)
        almacen.save()
        almacen.estantes.bulk_create(registros)

class UnidadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ("__all__")
        read_only_fields = ("estado", "codigo", "producto")

class UnidadSerializer(UnidadListSerializer):
    cantidad = serializers.FloatField(required=True)
    class Meta(UnidadListSerializer.Meta):
        model = Unidad
        fields = ("unidad", "estante", "estado", "codigo", "cantidad")
        read_only_fields = ("estado", "codigo", "producto")

    @transaction.atomic
    def create(self, data):
        detalle = data.get("unidad")
        cantidad = self.data.pop("cantidad")
        data.pop("cantidad")
        self.validar_cantidad(detalle, cantidad)
        return self.registrar_unidad(cantidad, data, detalle)

    def registrar_unidad(self, cantidad, datos, detalle):
        producto = detalle.producto
        for i in range(int(cantidad)):
            unidad = Unidad(**datos, producto=producto.id,
                            codigo=uuid.uuid4(),
                            fecha=detalle.fecha)
            unidad.save()
            producto.cantidad = producto.cantidad + 1
            detalle.cantidad_procesada = detalle.cantidad_procesada + 1
        detalle.save()
        producto.save()
        return unidad

    def validar_cantidad(self, detalle, cantidad):
        disponible = detalle.faltante_por_procesar
        if cantidad == disponible:
            raise ProductoProcesadoError()
        if cantidad > disponible:
            raise CantidadInvalidadError()
