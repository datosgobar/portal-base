#!/bin/bash
set -eu
## DESCRIPTION: Setear los diferentes estados de mantenimiento.

## AUTHOR: Jose A. Salgado

# Locaciones:
BASE_FOLDER="/etc/portal-modes/"
FILE_FLAG="$BASE_FOLDER/status"
ERR_VIEWS_FOLDER="$BASE_FOLDER/views"

# Vistas de error:
# Sobre carga, demasiadas visitas: "muchas-visitas.html"
# Problema tecnico, error general: "problemas-tecnicos.html"
# Trabajando en el sitio, mejorandolo: "mejorando-el-sitio.html"

# Vista de NO-ERROR
DEFAULT_ERROR_VIEW="default.html"


# Mensaje de ayuda
HELPME="Utilizar: $ ./set_status.sh [ mejorando-el-sitio | problemas-tecnicos | muchas-visitas ]."

usage(){
   echo  $HELPME;
}

function set_action(){
    rm -rf $FILE_FLAG.*
    touch "$FILE_FLAG.fail"
  if [[ ! "$ACTION" == "ok" ]] ; then
    cp "$ERR_VIEWS_FOLDER/$ACTION.html" "$ERR_VIEWS_FOLDER/$DEFAULT_ERROR_VIEW"
  else
     rm -rf $FILE_FLAG.*
     touch "$FILE_FLAG.ok"
  fi
printf " ... hecho!\n"
}

function is_in_list {
  local list="$1"
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    result=0
  else
    result=1
  fi
  return $result
}

# ARGS
ACEPTABLE_ARGS="mejorando-el-sitio problemas-tecnicos muchas-visitas ok"
ACTION=''
printf "Portal Mode:\n===========\n"
if [ $# -gt 0 ] ; then
    if `is_in_list "$ACEPTABLE_ARGS" "$1"`  ; then
        echo "Ejecutanto cambio a modo: '$1'.";
        ACTION=$1
    else
        if [[ ! "$1"  == "--help" ]]; then
              printf "\nOops! '$1': no es un argumento valido...\n$HELPME\n";
        fi
    fi
else
    printf "Error: Falta argumento requerido, debe indicar un modo.\n$HELPME\n";
    exit 1
fi

# SET
case $1 in
    "muchas-visitas") printf "Pasando a modo \"Sobre carga de visitas\""; set_action ;;
    "problemas-tecnicos") printf "Pasando a modo \"Trabajando en un Error\""; set_action ;;
    "mejorando-el-sitio") printf "Pasando a modo \"Mejorando el Sitio\""; set_action ;;
    "ok") printf "Volviendo a ejecucion normal."; set_action ;;
    "--help") usage 2>&1;;
    esac
