# Instalación de portales

## Pre-requisitos

Previo a la instalacion, prepararemos el entorno:

    mkdir ~/mi_portal/
    sudo ln -s ~/mi_portal/ /etc/mi_portal
    cd ~/mi_portal/

## Instalacion

La instalación de portales puede ser llevada a cabo mediantes el script `deploy/install.py`.
Este script requerirá ciertos parámetros para completar la instalación:

+ --`error_email`
  - description: EMail donde se enviarán los errores de la aplicación.
  - required: True
  - default: None
+ --`site_host`  
  - description: IP o dominio de la aplicación.
  - required: True
+ --`database_user`
  - description: Usuario de la base de datos a crear.
  - required: True
  - default: None
+ --`database_password`
  - description: Contraseña de la base de datos a crear.
  - required: True
  - default: None
+ --`datastore_user`
  - description: Usuario del "datastore" de ckan a crear.
  - required: True
  - default: None
+ --`datastore_password`
  - description: Contraseña del "datastore" de ckan a crear.
  - required: True
  - default: None

+ --`repo`
  - description: portal_datos.gob.ar o portal-andino
  - required: False
  - default: portal-andino

+ --`branch`
  - description: tag o branch a instalar de la aplicación.
  - required: False
  - default: master

+ --`nginx_port`
  - description: Puerto sobre el que escuchara NGINX.
  - required: False
  - default: 80

+ --`datastore_port`
  - description: Puerto para DataPusher.
  - required: False
  - default: 8800

Por comodidad, utilizaremos variables de entorno para completar los argumentos requeridos.

```bash
ERROR_EMAIL=errors@email.com
SITE_HOST=http://un-dominio.com
DATABASE_USER=my_default_db_user
DATABASE_PASSWORD=my_default_db_user_pass
DATASTORE_USER=my_datastore_db_user
DATASTORE_PASSWORD=my_datastore_db_user_pass
```

Luego, lanzaremos la instalacion:

```bash
# Asumo que se esta en /etc/mi_portal
# Descargamos el instalador
wget https://raw.github.com/datosgobar/portal-base/master/deploy/install.py
python ./install.py --error_email "$ERROR_EMAIL" \
                    --site_host "$SITE_HOST" \
                    --database_user "$DATABASE_USER" \
                    --database_password "$DATABASE_PASSWORD" \
                    --datastore_user "$DATASTORE_USER" \
                    --datastore_password "$DATASTORE_PASSWORD" \
                    --repo portal_datos.gob.ar

# Inicializar el portal a sus valores productipor omision.
docker-compose -f latest.yml exec portal bash /etc/ckan_init.d/init_datosgobar.sh
```

_El script tiene el comportamiento predeterminado de instalar la *última versión* de **portal-andino**._
