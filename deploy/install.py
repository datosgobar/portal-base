#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
from os import path

parser = argparse.ArgumentParser(description='Instalar andino or datosgobar con docker.')

parser.add_argument('--error_email', required=True)
parser.add_argument('--site_host', required=True)
parser.add_argument('--database_user', required=True)
parser.add_argument('--database_password', required=True)
parser.add_argument('--datastore_user', required=True)
parser.add_argument('--datastore_password', required=True)
parser.add_argument('--nginx_port', default="80")
parser.add_argument('--datastore_port', default="8800")
parser.add_argument('--repo', choices=['portal-andino', 'portal_datos.gob.ar'], default='portal-andino')
parser.add_argument('--branch', default='master')

args = parser.parse_args()

COMPOSE_FILE_URL = "https://raw.githubusercontent.com/datosgobar/%s/%s/latest.yml" % (args.repo, args.branch)


def check_docker():
    subprocess.check_call([
        "docker",
        "ps"
    ])


def check_compose():
    subprocess.check_call([
        "docker-compose",
        "--version",
    ])


def get_compose_file(base_path):
    compose_file = "latest.yml"
    compose_file_path = path.join(base_path, compose_file)
    subprocess.check_call([
        "curl",
        COMPOSE_FILE_URL,
        "--output",
        compose_file_path
    ])
    return compose_file_path


def configure_env_file(base_path):
    env_file = ".env"
    env_file_path = path.join(base_path, env_file)
    with open(env_file_path, "w") as env_f:
        env_f.write("POSTGRES_USER=%s\n" % args.database_user)
        env_f.write("POSTGRES_PASSWORD=%s\n" % args.database_password)
        env_f.write("NGINX_HOST_PORT=%s\n" % args.nginx_port)
        env_f.write("DATASTORE_HOST_PORT=%s\n" % args.datastore_port)


def init_application(compose_path):
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "up",
        "-d",
        "nginx",
    ])


def configure_application(compose_path):
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "exec",
        "-T",
        "portal",
        "/etc/ckan_init.d/init.sh",
        "-e", args.error_email,
        "-h", args.site_host,
        "-p", args.database_user,
        "-P", args.database_password,
        "-d", args.datastore_user,
        "-D", args.datastore_password,
    ])


print("[ INFO ] Comprobando que docker esté instalado...")
check_docker()
print("[ INFO ] Comprobando que docker-compose este instalado...")
check_compose()
print("[ INFO ] Descargando archivos necesarios...")
directory = path.dirname(path.realpath(__file__))
compose_file_path = get_compose_file(directory)
print("[ INFO ] Escribiendo archivo de configuración del ambiente (.env) ...")
configure_env_file(directory)
print("[ INFO ] Iniciando la aplicación")
init_application(compose_file_path)
print("[ INFO ] Espetando a que la base de datos este disponible...")
time.sleep(10)
print("[ INFO ] Configurando...")
configure_application(compose_file_path)
print("[ INFO ] Listo.")
