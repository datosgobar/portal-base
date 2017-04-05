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
parser.add_argument('--repo', choices=['portal-andino', 'portal_datos.gob.ar'], default='portal-andino')
parser.add_argument('--branch', default='development')

args = parser.parse_args()

COMPOSE_FILE_URL = "https://raw.githubusercontent.com/datosgobar/%s/%s/latest.yml" % (args.repo, args.branch)

print("[ INFO ] Comprobando que docker esté instalado...")

subprocess.check_call([
    "docker",
    "ps"
])

print("[ INFO ] Comprobando que docker-compose este instalado...")

subprocess.check_call([
    "docker-compose",
    "--version",
])

print("[ INFO ] Descargando archivos necesarios...")

directory = path.dirname(path.realpath(__file__))

compose_file = "lasted.yml"
env_file = ".env"
compose_file_path = path.join(directory, compose_file)
env_file_path = path.join(directory, env_file)

subprocess.check_call([
    "curl",
    COMPOSE_FILE_URL,
    "--output",
    compose_file_path
])

print("[ INFO ] Escribiendo archivo de configuración del ambiente (.env) ...")

with open(env_file_path, "w") as env_f:
    env_f.write("POSTGRES_USER=%s\n" % args.database_user)
    env_f.write("POSTGRES_PASSWORD=%s\n" % args.database_password)

print("Starting up site")
subprocess.check_call([
    "docker-compose",
    "-f",
    compose_file_path,
    "up",
    "-d",
    "nginx",
])

print("[ INFO ] Espetando a que la base de datos este disponible...")

time.sleep(10)

subprocess.check_call([
    "docker-compose",
    "-f",
    compose_file_path,
    "exec",
    "portal",
    "/etc/ckan_init.d/init.sh",
    "-e", args.error_email,
    "-h", args.site_host,
    "-p", args.database_user,
    "-P", args.database_password,
    "-d", args.datastore_user,
    "-D", args.datastore_password,
])
