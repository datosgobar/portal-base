# Portal base

Imagen basada en para los portales [andino](https://github.com/datosgobar/portal-andino) y datosgobar.

Contiene la instalación base de [Ckan](https://github.com/ckan/ckan) y los scripts especificos para los portales.

Actualmente ckan-2.3.5


## Scripts disponibles:

Todos los scripts estan en la carpeta /etc/ckan_init.d/ *dentro* del container.
Dado un script llamado `init.sh`, puede ser ejecutado de la forma:

    docker exec *container* -it /etc/ckan_init.d/init.sh
    
* Agregar administrador del sitio: `add_admin.sh $ADMIN_USERNAME`
* Cambiar la url del datapusher: `change_datapusher_url $IP_O_HOST`
* Inicializar la aplicacion: `init.sh ...` (Ver parametro más abajo)
* Correr comando en paster: `paster.sh <comando>` (por ejemplo: `paster.sh --plugin=ckan db init`)
* Actualizar configuracion del `production.ini`: `update_conf.sh <key>=<value>`


## Inicializacion:

Para inicializar las bases de datos, se debe usar el script `init.sh`. El mismo espera los siguientes parametros:

    Usage: init.sh
    (-u datapusher_host)
    (-e error_email_from)
    (-h site_host or ip)
    (-p database_user) (-p database_password)
    (-d datastore_user) (-D datastore_password)

Un ejemplo de su uso:

    docker exec -it andino /etc/ckan_init.d/init.sh \
        -u 172.19.0.6 \
        -e admin@example.com \
        -h midominio.com \
        -p usuario_db \
        -P password_db \
        -d usuario_datastore_db \
        -D password_datastore_db
        
## En Desarrollo:

Existe un script que setea los defaults en desarrollo:

    docker exec -it andino /etc/ckan_init.d/init_dev.sh
