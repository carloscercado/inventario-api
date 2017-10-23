from django.conf.urls import url, include
from django.contrib import admin
from productos import views as pro
from ubicacion import views as ubi
from ventas import views as ven
from compras import views as com
from .enrrutador import RaizRouter
from rest_framework.documentation import include_docs_urls
import debug_toolbar

router = RaizRouter(trailing_slash=False)

router.register(r'productos', pro.ProductoVista)
router.register(r'categorias', pro.CategoriaVista)
router.register(r'almacenes', ubi.AlmacenVista)
router.register(r'estantes', ubi.EstanteVista)
router.register(r'compras', com.CompraVista)
router.register(r'proveedores', com.ProveedorVista)
router.register(r'ventas', ven.VentaVista)
router.register(r'clientes', ven.ClienteVista)
router.register(r'unidades', ubi.UnidadVista)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Documentacion')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]