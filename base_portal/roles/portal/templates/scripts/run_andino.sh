#!/bin/sh
set -e

service supervisor start
cron

. /etc/apache2/envvars
exec /usr/sbin/apache2 -D FOREGROUND
