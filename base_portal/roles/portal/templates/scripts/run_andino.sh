#!/bin/sh
set -e

service supervisor start

. /etc/apache2/envvars
exec /usr/sbin/apache2 -D FOREGROUND
