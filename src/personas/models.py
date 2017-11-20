from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="usuario")
    nombre = models.CharField(max_length=20, help_text="nombre del usuario")
    apellido = models.CharField(max_length=20, help_text="apellido del usuario")
    direccion = models.CharField(max_length=80, null=True,
                                 help_text="direccion del usuario")
    telefono = models.CharField(max_length=15, null=True,
                                help_text="telefono del usuario")
    pregunta = models.CharField(max_length=60, help_text="pregunta de seguridad")
    respuesta = models.CharField(max_length=60, help_text="respuesta de seguridad")
    cargo = models.CharField(max_length=15, null=True,
                                help_text="cargo del usuario")

    def __str__(self):
        return self.nombre + " " + self.apellido
