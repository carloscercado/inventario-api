from rest_framework import serializers
from .models import Almacen, Seccion, Unidad
from django.db import transaction
from .exceptions import CantidadInvalidadError, ProductoProcesadoError
import uuid

class AlmacenSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='almacen-detail', format='html')
    class Meta:
        model = Almacen
        fields = ("__all__")
        read_only_fields = ("eliminable", "volumen")


class SeccionAlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = ("id", "nombre", "volumen", "volumen_restante",
                  "longitud", "altura", "anchura", "almacen")
        read_only_fields = ("volumen","volumen_restante")

    @transaction.atomic
    def create(self, data):
        seccion = Seccion(**data)
        seccion.volumen_restante = seccion.volumen
        seccion.save()
        return seccion

class SeccionSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerializer
    detalle = serializers.HyperlinkedIdentityField(view_name='seccion-detail', format='html')
    class Meta:
        model = Seccion
        fields = ("id", "nombre", "volumen", "volumen_restante", "detalle",
                  "longitud", "altura", "anchura")
        read_only_fields = ("volumen","volumen_restante")

    @transaction.atomic
    def create(self, data):
        seccion = Seccion(**data)
        seccion.volumen_restante = seccion.volumen
        seccion.save()
        return seccion

class AlmacenDetalleSerializer(serializers.ModelSerializer):
    secciones = SeccionSerializer(many=True)
    class Meta:
        model = Almacen
        fields = ("id", "nombre", "direccion", "telefono", "secciones")
        #read_only_fields = ("eliminable", "estantes", "detalle")

    @transaction.atomic
    def create(self, datos):
        secciones = datos.pop("secciones")
        almacen = Almacen.objects.create(**datos)
        self.registrar_secciones(almacen, secciones)
        return almacen

    @transaction.atomic
    def update(self, almacen, datos):
        seciones = datos.pop("seciones")
        for key, value in datos.items():
            setattr(almacen, key, value)
        #almacen.borrar_seciones()
        #self.registrar_seciones(almacen, estantes)
        return almacen

    def registrar_secciones(self, almacen, secciones):
        registros = []
        for i in secciones:
            seccion = Estante(**i, almacen=almacen,
                              capacidad_restante=i.get("capacidad_total"))
            registros.append(seccion)
        almacen.save()
        almacen.secciones.bulk_create(registros)

class UnidadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ("__all__")
        read_only_fields = ("estado", "codigo", "producto")

class UnidadSerializer(UnidadListSerializer):
    cantidad = serializers.FloatField(required=True)
    class Meta(UnidadListSerializer.Meta):
        model = Unidad
        fields = ("unidad", "seccion", "estado", "codigo", "cantidad")
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
