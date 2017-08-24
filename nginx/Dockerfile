FROM nginx:1.11.9
MAINTAINER Leandro Gomez<lgomez@devartis.com>

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY command.sh .
CMD ["bash", "command.sh"]

RUN ansible-playbook -i "localhost," -c local modes.yml
COPY scripts/set_status.sh /etc/portal-modes/scripts
