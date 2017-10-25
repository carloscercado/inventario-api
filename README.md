

# API Inventario

El diseño de grandes aplicaciones para empresas está evolucionando de arquitecturas [monolíticas](https://tallerbd.wikispaces.com/Arquitectura+Monol%C3%ADtica.)  a  arquitecturas  basadas  en  [microservicios](https://es.wikipedia.org/wiki/Arquitectura_de_microservicios).  Estas  son  particularmente adecuadas  para  ejecutarse  en  entornos [cloud](https://es.wikipedia.org/wiki/Computación_en_la_nube)  porque  cada  servicio  puede  ser desarrollado,  desplegado  y  gestionado  individualmente,  lo  que  permite  un  control mucho más detallado y un alto grado de **escalabilidad**.
 
Basado en un ejemplo concreto, se desarrolló un sistema para la gestion de Inventarios bajo una arquitectura de microservicios, mostrando los desafíos de ésta en un entorno de intranet, pero que puede ser facilmente acoplado a un entorno cloud.

Para el desarrollo de esta API se utilizó [Python](https://es.wikipedia.org/wiki/Python) como lenguaje de programación y el Framework [Django Rest Framework](www.django-rest-framework.org) para la creacion de todos los [End Point](https://en.wikipedia.org/wiki/Web_API#Endpoints) del API.

## Instalación

### Quick start

Clona el proyecto en el local:

    1. $ git clone https://github.com/carloscercado/inventario-api

Cambia al directorio raiz del proyecto:

    1. $ cd inventario-api

Instala las dependencias:

    1. $ pip install -r requirements.txt

Configura las credenciales de conexion a la base de datos en el archivo [**settings.py**](https://github.com/carloscercado/inventario-api/blob/master/src/inventario/settings.py)

    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2', 
                'NAME': 'inventario', #base de datos                     
                'USER': 'postgres', #nombre de usuario
                'PASSWORD': 'admin', #clave
                'HOST': 'localhost',    #servidor                  
                'PORT': '5432',  #puerto                   
            }
    }

Corre las migraciones:

    1. python src/manage.py migrate

### Documentacion del API

Para ver la documentacion del API debe correr el servidor

    1. $ python src/manage.py runserver

Luego, en su navegador dirijase a la direccion http://127.0.0.1:8000/docs

### Instrucciones detalladas

Para mas informacion sobre funcionamiento de las herramientas utilizadas en el proyecto visitar:
[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
[2]: https://www.django-rest-framework.org/
