Supervise las direcciones IP sondeándolas a través de solicitudes ICMP (ping).

Una aplicación web está disponible usando Flask para ver los estados de las direcciones IP y el historial de encuestas.

El sondeo se ejecuta como un servicio como parte de la aplicación web.

Una base de datos SQLite se utiliza para almacenar hosts, resultados de encuestas, cuentas de usuario, etc.

# Configuración

Deberán realizarse las siguientes configuraciones para poder realizar la configuración:

## 1) Instalar Python

Es necesario instalar Python 3.0+, puede encontrar instaladores [aquí] (https://www.python.org/downloads/)

## 2) Instalar los requisitos de Python

Desde el directorio principal de este repositorio, ejecute el siguiente comando:

''
pip install -r requirements.txt
''

## 3) Configuración

Siga las instrucciones a continuación para ejecutar el servidor web y navegue hasta el servidor una vez que se esté
ejecutando. Serás redirigido a una página de configuración para realizar la configuración inicial en la aplicación web /
base de datos.

*** Nota: *** Configurará una cuenta de administrador durante la instalación, esta cuenta deberá utilizarse para obtener
todas las funciones. De forma predeterminada, los visitantes no autenticados solo podrán ver los estados de IP

# Ejecutando servidor web

Para ejecutar el servidor web de la forma más básica (perezosa), puede ejecutar lo siguiente desde el directorio
principal de este repositorio:

''
flask run
''

Si no se proporcionan argumentos, el servidor web se ejecutará en *** http: //127.0.0.1: 5000 ***

Si desea especificar un host / puerto, puede utilizar los siguientes argumentos:

''
flask run -h <host> -p <puerto>
''

Para ver todos los argumentos:

''
flask run --help
''

*** Nota: *** Sería prudente trasladar esto a un servidor WSGI para uso en producción,
ver [aquí] (https://flask.palletsprojects.com/en/1.1.x/deploying/)

## 4) Migraciones de bases de datos

En caso de que el esquema de la base de datos cambie, será necesario realizar una migración. Estas migraciones se pueden
encontrar en `migraciones / versiones /`

Para realizar una migración de base de datos, detenga los servicios web y luego ejecute el siguiente comando desde el
directorio principal de este repositorio:

''
flask db upgrade
''

# FUNCIONES DE LA APLICACION

* Agregar administración de usuarios en la configuración
    * Agregar usuario
    * Eliminar usuario
    * Restablecer la contraseña
* Permitir agregar hosts por nombre de host
    * nslookup para encontrar la dirección IP
    * Falla y omite la adición de host si nslookup falla
