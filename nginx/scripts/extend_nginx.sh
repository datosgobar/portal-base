#!/usr/bin/env sh
set -e;

if ! grep -q "root_location.conf" "/etc/nginx/conf.d/default.conf"; then
    var=$(grep -n 'location / {' /etc/nginx/conf.d/default.conf | awk -F  ":" '{print $1}')
    let "var=var+1"
    sed -i "${var}i    include $NGINX_AVAILABLE_SITES/extras/extended_cache/root_location.conf;" /etc/nginx/conf.d/default.conf
fi

if ! grep -q "purge_location.conf" "/etc/nginx/conf.d/default.conf"; then
    var=$(grep -n 'location / {' /etc/nginx/conf.d/default.conf | awk -F  ":" '{print $1}')
    sed -i "${var}i    include $NGINX_AVAILABLE_SITES/extras/extended_cache/purge_location.conf;" /etc/nginx/conf.d/default.conf
fi

if ! grep -q "server_tokens off;" "/etc/nginx/conf.d/default.conf"; then
    sed -i "1i    server_tokens off;" /etc/nginx/conf.d/default.conf
fi
