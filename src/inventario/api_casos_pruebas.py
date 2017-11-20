from rest_framework.test import APITestCase
from personas.models import Persona
from django.contrib.auth.models import User

class APICasoPrueba(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username="admin", password="admin")
        self.usuario = Persona.objects.create(user_id=user.id, nombre="carlos", apellido="cercado",
                                         pregunta="abc", respuesta="abcdario", cargo="jefe")

        self.client.credentials(HTTP_AUTHORIZATION='Basic YWRtaW46YWRtaW4=')

    def tearDown(self):
        User.objects.all().delete()