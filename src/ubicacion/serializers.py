from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Almacen, Seccion, Unidad
from django.db import transaction
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
        secciones = datos.pop("secciones")
        for key, value in datos.items():
            setattr(almacen, key, value)
        #almacen.borrar_seciones()
        #self.registrar_seciones(almacen, estantes)
        return almacen

    def registrar_secciones(self, almacen, secciones):
        registros = []
        for i in secciones:
            seccion = Seccion(**i, almacen=almacen)
            seccion.volumen_restante = seccion.volumen
            registros.append(seccion)
        almacen.save()
        almacen.secciones.bulk_create(registros)

class UnidadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ("__all__")

class UnidadSerializer(UnidadListSerializer):
    class Meta(UnidadListSerializer.Meta):
        model = Unidad
        fields = ("id","unidad", "seccion", "volumen", "estado", "codigo",
                   "altura", "longitud", "ancho",)
        read_only_fields = ("estado", "codigo", "producto", "volumen")

class UnidadCreateSerializer(UnidadListSerializer):
    cantidad = serializers.FloatField(required=True)
    class Meta(UnidadListSerializer.Meta):
        model = Unidad
        fields = ("id","unidad", "seccion", "volumen", "estado", "codigo", "cantidad",
                   "altura", "longitud", "ancho",)
        read_only_fields = ("estado", "codigo", "producto", "volumen")

    @transaction.atomic
    def create(self, data):
        detalle = data.get("unidad")
        cantidad = self.data.pop("cantidad")
        data.pop("cantidad") # quitarlo de validated_data
        return self.registrar_unidad(cantidad, data, detalle)

    def registrar_unidad(self, cantidad, datos, detalle):
        self.validar_cantidad(detalle, cantidad)
        producto = detalle.producto
        for i in range(int(cantidad)):
            unidad = Unidad(**datos, producto=producto.id,
                            codigo=uuid.uuid4().hex,
                            fecha=detalle.fecha)
            unidad.save()
            seccion = unidad.seccion
            self.validar_disponibilidad_seccion(seccion, unidad.volumen)
            seccion.volumen_restante = seccion.volumen_restante - unidad.volumen
            seccion.save()
            producto.cantidad = producto.cantidad + 1
            detalle.cantidad_procesada = detalle.cantidad_procesada + 1
        detalle.save()
        producto.save()
        return unidad

    def validar_cantidad(self, detalle, cantidad):
        disponible = detalle.faltante_por_procesar
        if cantidad == disponible:
            error = {
                "cantidad": "invalida. No hay productos para procesar"
            }
            raise ValidationError(error)
        if cantidad > disponible:
            error = {
                "cantidad": "invalida. Es mayor a la disponible ["+str(disponible)+"]"
            }
            raise ValidationError(error)

    def validar_disponibilidad_seccion(self, seccion, volumen):
        disponible = seccion.volumen_restante
        if volumen > disponible:
            error = {
                "cantidad": "el espacio disponible en la seccion escogida no es suficiente",
                "seccion": "disponible en seccion ["+str(disponible)+"] - volumen a ubicar ["+str(volumen)+"]"
            }
            raise ValidationError(error)