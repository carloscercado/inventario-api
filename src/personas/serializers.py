from rest_framework import serializers
from .models import Persona
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class UsuarioSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='persona-detail', format='html')
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    telefono = serializers.RegexField(r'[0-9]{3}[-][0-9]{7}$', max_length=11, min_length=11)
    class Meta:
        model = Persona
        exclude = ('user',)


    def create(self, datos):
        username = datos.pop('username')
        password = datos.pop('password')
        email = datos.pop('email')

        user = User.objects.create_user(username=username, password=password,
                                        email=email)
        usuario = Persona.objects.create(user=user, **datos)
        usuario.username = username
        usuario.password = "******************"
        usuario.email = email
        return usuario

class UsuarioListSerializer(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='persona-detail', format='html')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Persona
        exclude = ('user', 'respuesta',)



