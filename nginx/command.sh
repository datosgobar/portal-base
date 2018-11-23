#!/usr/bin/env sh
set -e;

rm -f /etc/nginx/conf.d/default.conf;

if [[ -n "$NGINX_CONFIG_FILE" \
    && -f "$NGINX_SSL_CONFIG_DATA/andino.key" \
    && -f "$NGINX_SSL_CONFIG_DATA/andino.crt" ]]; then
    echo "Using '$NGINX_CONFIG_FILE' configuration"
    ln -s "$NGINX_AVAILABLE_SITES/$NGINX_CONFIG_FILE" /etc/nginx/conf.d/default.conf;
    openssl dhparam 2048 -out $NGINX_SSL_CONFIG_DATA/andino_dhparam.pem;
    sed -i "s/SSL_PORT_NUMBER/${NGINX_HOST_SSL_PORT}/g" /etc/nginx/conf.d/default.conf
else
    echo "Using '$NGINX_DEFAULT_CONFIG_FILE' default configuration"
    ln -s "$NGINX_AVAILABLE_SITES/$NGINX_DEFAULT_CONFIG_FILE" /etc/nginx/conf.d/default.conf;
fi

# Configure extended cache if specified
if [ "$NGINX_EXTENDED_CACHE" = 'yes' ] ; then
    chmod -R u+rwx $NGINX_SCRIPTS
    "$NGINX_SCRIPTS"/extend_nginx.sh ;
fi

# Configure max_size cache option
max_size="$NGINX_DEFAULT_CACHE_MAX_SIZE";
if [[ -n "$NGINX_CACHE_MAX_SIZE" ]]; then
    max_size="$NGINX_CACHE_MAX_SIZE";
fi
sed -i "s/max_size=[[:alnum:]]*/max_size=$max_size/" /etc/nginx/conf.d/default.conf


# Configure inactive cache option
inactive="$NGINX_DEFAULT_CACHE_INACTIVE";
if [[ -n "$NGINX_CACHE_INACTIVE" ]]; then
    inactive="$NGINX_CACHE_INACTIVE";
fi
sed -i "s/inactive=[[:alnum:]]*/inactive=$inactive/" /etc/nginx/conf.d/default.conf


echo "Stating nginx (with openresty)...";
/usr/local/openresty/bin/openresty -g "daemon off;";
