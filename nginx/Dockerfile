FROM nginx:1.11.9
MAINTAINER Leandro Gomez<lgomez@devartis.com>

RUN mkdir /webapps/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY command.sh .
COPY maintenance_on.html /webapps/
CMD ["bash", "command.sh"]
