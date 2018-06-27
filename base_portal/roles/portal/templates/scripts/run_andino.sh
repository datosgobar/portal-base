#!/bin/sh
set -e

. /etc/apache2/envvars
exec /usr/sbin/apache2 -D FOREGROUND

exec sudo apt-get update
exec sudo apt-get -y install supervisor
exec sudo cp /etc/ckan/default/supervisor-ckan-worker.conf /etc/supervisor/conf.d
exec echo "Traje el archivo supervisor-ckan-worker.conf (con exec)"
exec echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo ""
exec sudo service supervisor restart

RUN sudo apt-get update
RUN sudo apt-get -y install supervisor
RUN sudo cp /etc/ckan/default/supervisor-ckan-worker.conf /etc/supervisor/conf.d
RUN echo "Traje el archivo supervisor-ckan-worker.conf (con RUN)"
RUN echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo "" exec echo ""
RUN sudo service supervisor restart