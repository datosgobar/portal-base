FROM nginx:1.11.9
MAINTAINER Leandro Gomez<lgomez@devartis.com>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
      apt-get install software-properties-common libffi-dev libssl-dev python python-dev python-pip -y
RUN pip install --upgrade cffi && pip install ansible && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY command.sh .
CMD ["bash", "command.sh"]

COPY modes.yml /etc/portal-modes/modes.yml
RUN ansible-playbook -i "localhost," -c local /etc/portal-modes/modes.yml
COPY scripts/set_status.sh /etc/portal-modes/scripts
RUN apt-get remove --purge software-properties-common libffi-dev libssl-dev python python-dev python-pip -y
