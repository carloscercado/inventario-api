from django.conf.urls import url, include
from django.contrib import admin
from productos import views as pro
from ubicacion import views as ubi
from salidas import views as sal
from compras import views as com
from .enrrutador import RaizRouter
import debug_toolbar
from rest_framework_swagger.views import get_swagger_view

documentacion = get_swagger_view()

router = RaizRouter(trailing_slash=False)

router.register(r'productos', pro.ProductoVista)
router.register(r'categorias', pro.CategoriaVista)
router.register(r'almacenes', ubi.AlmacenVista)
router.register(r'secciones', ubi.SeccionVista)
router.register(r'compras', com.CompraVista)
router.register(r'proveedores', com.ProveedorVista)
router.register(r'salidas', sal.SalidaVista)
router.register(r'dependencias', sal.DependenciaVista)
router.register(r'unidades', ubi.UnidadVista)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', documentacion),
    url(r'^__debug__/', include(debug_toolbar.urls))
    ]