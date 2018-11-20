FROM openresty/openresty:1.13.6.2-alpine
MAINTAINER Leandro Gomez<lgomez@devartis.com>

ENV NGINX_AVAILABLE_SITES=/etc/nginx/site-available \
    NGINX_DEFAULT_CONFIG_FILE=nginx.conf \
    NGINX_SSL_CONFIG_FILE=nginx_ssl.conf \
    NGINX_DEFAULT_CACHE_MAX_SIZE=1g \
    NGINX_DEFAULT_CACHE_INACTIVE=240m \
    NGINX_SSL_CONFIG_DATA=/etc/nginx/ssl

RUN mkdir -p $NGINX_AVAILABLE_SITES
COPY configs/ $NGINX_AVAILABLE_SITES
COPY command.sh .

CMD ["sh", "command.sh"]
