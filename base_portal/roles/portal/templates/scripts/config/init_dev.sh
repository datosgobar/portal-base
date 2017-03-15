#!/usr/bin/env bash
current_dir="$(dirname "$0")"
CKAN_IP=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')

"$current_dir/init.sh" -u "$CKAN_IP" -e admin@example.com -h localhost -p ckan -P ckan -d ckan_datastore -D ckan_datastore
