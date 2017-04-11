# Forma de llevar a cabo un _release_

## Todos los portales

Los _releases_ son llevados a cabo mediante _tags_ de _git_.

En principio, una nueva funcionaliadad debe ser implementada en un _branch_ de _git_.
Luego de terminada la misma, debe crearse un _pull-request_ y esperar a ser evaluado y aceptado.
Cuando se acepta un _pull-request_ debe "mergearse" al _branch master_.

Para sacar una nueva version del portal base, basta con crear un nuevo _tag_ con incrementando la version correspondiente.
El formato del tag _siempre debe ser x.x.x_, donde cada _x_ corresponde a Mayor.Minor.Patch
Un ejemplo podria ser:

    git tag 0.2 -m "Version 0.2 del portal base"
    git push --tags

Este procedimiento generará una nueva imagen en [docker.hub](https://hub.docker.com/r/datosgobar/portal-datos.gob.ar/builds/), la cual estara disponible para ser usada.

## Portal base

Este portal contiene 3 `Dockerfile`s:
- portal-base
- nginx
- solr

Cada vez que se genere un nuevo _release_, se generaran las imagenes para los 3.

## Portal andino y Portal datos.gob.ar

### Cambios en cada portal
Estos portales extienden de una version especifica del portal base. 
Esto se ve reflejado en el `Dockerfile` de cada portal:
    
    FROM datosgobar/portal-base:release-0.1

Ademas cada portal tiene su propia version. La misma debe verse reflejada en el archivo `latest.yml` con el fin de establecer la ultima version estable de la aplicacion.

Tomando como ejemplo el portal-andino, el mismo define que el servicio **portal** usa una imagen `datosgobar/portal-andino:release-0.1`.
Para hacer un nuevo release, debe __primero subirse la nueva version__ y luego que se genero la nueva Imagen, cambiar el archivo `latest.yml`. 

Por ejemplo, para sacar una verion `0.2`:

    git tag 0.2 -m "Version 0.2 del portal andino"
    git push --tags

Esperamos a que se genere la imagen, luego cambiamos la imagen del servicio "portal" en el archivo `latest.yml` a `datosgobar/portal-andino:release-0.2`. y pusheamos el codigo al master del proyecto.


### Actualizar un proyecto

Para actualizar un proyecto, debe correrse el script `update.py` en el mismo directorio donde se instalo la aplicacion.

    wget https://raw.github.com/datosgobar/portal-base/master/deploy/update.py

    REPO=portal-andino # Podria ser portal_datos.gob.ar
    VERSION=0.2 # O a la que querramos actualizar
    python update.py --repo $REPO --branch $VESION
