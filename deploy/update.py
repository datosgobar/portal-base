#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
from os import path

parser = argparse.ArgumentParser(description='Actulizar andino or datosgobar con docker.')

parser.add_argument('--repo', choices=['portal-andino', 'portal_datos.gob.ar'], default='portal-andino')
parser.add_argument('--branch', default='development')

args = parser.parse_args()

REPOS = {
    "portal-andino": {
        "containers": ['andino-nginx', 'andino', 'andino-solr', 'andino-postfix', 'andino-redis', 'andino-db']
    },
    "portal_datos.gob.ar": {
        "containers": ['datosgobar-nginx', 'datosgobar', 'datosgobar-solr', 'datosgobar-postfix', 'datosgobar-redis', 'datosgobar-db']
    }
}

COMPOSE_FILE_URL = "https://raw.githubusercontent.com/datosgobar/%s/%s/latest.yml" % (args.repo, args.branch)

EXPECTED_CONTAINERS = REPOS[args.repo]['containers']


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


def reload_application(compose_path):
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "pull"
    ])
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "up",
        "-d",
        "nginx",
    ])


def check_previous_installation(base_path):
    compose_file = "latest.yml"
    compose_file_path = path.join(base_path, compose_file)
    if not path.isfile(compose_file_path):
        print("[ ERROR ] Por favor corra este comando en el mismo directorio donde instaló la aplicación")
        print("[ ERROR ] No se encontró el archivo %s en el directorio actual" % compose_file)
        raise Exception("[ ERROR ] No se encontró una instalación.")
    output = str(subprocess.check_output([
        "docker",
        "ps",
        "-a",
        "--format",
        "'{{.Names}}'"
    ]))
    local_containers = [container.strip("'") for container in output.split()]
    for container_name in EXPECTED_CONTAINERS:
        if container_name not in local_containers:
            print("[ ERROR ] El container %s no se encuentra en la aplicación." % container_name)
            print("[ ERROR ] Por favor instale la aplicación primero.")
            raise Exception("[ ERROR ] No se encontró una instalación.")


def post_update_commands(compose_path):
    pass


print("[ INFO ] Comprobando que docker esté instalado...")
check_docker()
print("[ INFO ] Comprobando que docker-compose este instalado...")
check_compose()
directory = path.dirname(path.realpath(__file__))
print("[ INFO ] Comprobando instalacion previa...")
check_previous_installation(directory)
print("[ INFO ] Descargando archivos necesarios...")
compose_file_path = get_compose_file(directory)
print("[ INFO ] Actualizando la aplicación")
reload_application(compose_file_path)
print("[ INFO ] Corriendo comandos post-instalación")
post_update_commands(compose_file_path)
print("[ INFO ] Listo.")
