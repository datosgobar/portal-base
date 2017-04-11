# Actualización de portales

La actualización de portales puede ser llevada a cabo mediantes el script `deploy/update.py`.
Para ello, puede descargarse y correrlo en línea de comando.

    wget https://raw.github.com/datosgobar/portal-base/master/deploy/update.py
    
    python ./update.py 
    
Acepta los siguientes parámetros, con sus correspondientes valores por defecto:

    --repo < portal_datos.gob.ar o portal-andino> default: portal-andino
    --branch < tag o branch a instalar de la aplicación > default: master

El script tiene el comportamiento predeterminado de actualizar a la *última versión* de **portal-andino**.

El comando debe ser corrido **en el lugar donde se instaló la aplicación**.

Por ejemplo, si se instaló la aplicación en `/etc/mi_portal`:

    cd /etc/mi_portal
    sudo wget https://raw.github.com/datosgobar/portal-base/master/deploy/update.py
    sudo python ./update.py
    
O si se instaló en alguna carpeta de un usuario:

    cd ~/mi_portal/
    wget https://raw.github.com/datosgobar/portal-base/master/deploy/update.py
    python ./update.py

