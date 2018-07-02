FROM openresty/openresty:1.13.6.2-alpine
MAINTAINER Leandro Gomez<lgomez@devartis.com>

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY command.sh .
CMD ["sh", "command.sh"]
