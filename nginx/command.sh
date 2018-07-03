#!/usr/bin/env sh
set -e;

rm -f /etc/nginx/conf.d/default.conf;
if [[ -n "$NGINX_CONFIG_FILE" ]]; then
    echo "Using '$NGINX_CONFIG_FILE' configuration"
    ln -s "$NGINX_AVAILABLE_SITES/$NGINX_CONFIG_FILE" /etc/nginx/conf.d/default.conf;
else
    echo "Using '$NGINX_DEFAULT_CONFIG_FILE' default configuration"
    ln -s "$NGINX_AVAILABLE_SITES/$NGINX_DEFAULT_CONFIG_FILE" /etc/nginx/conf.d/default.conf;
fi

echo "Stating nginx (with openresty)...";
/usr/local/openresty/bin/openresty -g "daemon off;";
