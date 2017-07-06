# Instalación de portales

La instalación de portales puede ser llevada a cabo mediantes el script `deploy/install.py`.
Para ello, puede descargarse y correrlo en línea de comando.

    wget https://raw.github.com/datosgobar/portal-base/master/deploy/install.py

    python ./install.py

Es script requerirá ciertos parámetros para completar la instalación:

    --error_email <email donde se enviarán los errores de la aplicación>
    --site_host <ip o dominio de la aplicación>
    --database_user <usuario de la base de datos a crear>
    --database_password <contraseña de la base de datos a crear>
    --datastore_user <usuario del "datastore" de ckan a crear>
    --datastore_password <contraseña del "datastore" de ckan a crear>

Además, acepta los siguientes parámetros, con sus correspondientes valores por defecto:

    --repo < portal_datos.gob.ar o portal-andino> default: portal-andino
    --branch < tag o branch a instalar de la aplicación > default: master
    --nginx_port < puerto > default: 80
    --datastore_port < puerto > default: 8800

El script tiene el comportamiento predeterminado de instalar la *última versión* de **portal-andino**.

El comando debe ser corrido **en el lugar donde se desea instalar la aplicación**.
Por ejemplo, si deseo instalar la aplicación en `/etc/mi_portal`:

    sudo mkdir /etc/mi_portal
    cd /etc/mi_portal
    sudo wget https://raw.github.com/datosgobar/portal-base/master/deploy/install.py
    sudo python ./install.py

O puedo instalarla en alguna carpeta de un usuario:

    mkdir ~/mi_portal/
    cd ~/mi_portal/
    wget https://raw.github.com/datosgobar/portal-base/master/deploy/install.py
    python ./install.py


## Portal andino

El script de instalación debería dejar la aplicación andando en el puerto `80`.

## Portal datos.gob.ar

Algunos comandos extras son necesarios para instalar completamente el portal.
Ver [la documentación del mismo](http://portal-datosgobar.readthedocs.io/es/latest/)
