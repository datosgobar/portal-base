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

# Configure max_size cache option
max_size="$NGINX_DEFAULT_CACHE_MAX_SIZE";
if [[ -n "$NGINX_CACHE_MAX_SIZE" ]]; then
    max_size="$NGINX_CACHE_MAX_SIZE";
fi
sed -i "s/max_size=[[:alnum:]]*[[:space:]]/max_size=$max_size /" /etc/nginx/conf.d/default.conf


# Configure inactive cache option
#inactive="$NGINX_DEFAULT_CACHE_INACTIVE";
#if [[ -n "$NGINX_CACHE_INACTIVE" ]]; then
#    inactive="$NGINX_CACHE_INACTIVE";
#fi
#sed -i "s/inactive=[^\s]*/inactive=$inactive /" /etc/nginx/conf.d/default.conf


echo "Stating nginx (with openresty)...";
/usr/local/openresty/bin/openresty -g "daemon off;";
