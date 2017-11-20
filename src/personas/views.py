from rest_framework import viewsets
from .models import Persona
from rest_framework.response import Response
from .serializers import UsuarioSerializer, UsuarioListSerializer


class UsuarioVista(viewsets.ModelViewSet):
    """
    list: lista todos los usuarios
    """

    queryset = Persona.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UsuarioSerializer
        return UsuarioListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.delete()
        return Response(status=204)

