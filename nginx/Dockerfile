FROM openresty/openresty:1.13.6.2-alpine
MAINTAINER Leandro Gomez<lgomez@devartis.com>

ENV NGINX_AVAILABLE_SITES=/etc/nginx/site-available \
    NGINX_DEFAULT_CONFIG_FILE=nginx.conf

RUN mkdir -p $NGINX_AVAILABLE_SITES
COPY configs/ $NGINX_AVAILABLE_SITES
COPY command.sh .

CMD ["sh", "command.sh"]
