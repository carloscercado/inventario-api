from django.conf.urls import url, include
from django.contrib import admin
from productos import views as pro
from ubicacion import views as ubi
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls


router = DefaultRouter(trailing_slash=False)

router.register(r'productos', pro.ProductoVista)
router.register(r'categorias', pro.CategoriaVista)
router.register(r'almacenes', ubi.AlmacenVista)
router.register(r'estantes', ubi.EstanteVista)



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Documentacion'))
]