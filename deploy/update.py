#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
from os import path

parser = argparse.ArgumentParser(description='Actulizar andino or datosgobar con docker.')

parser.add_argument('--repo', choices=['portal-andino', 'portal_datos.gob.ar'], default='portal-andino')
parser.add_argument('--branch', default='master')

args = parser.parse_args()

REPOS = {
    "portal-andino": {
        "containers": ['andino-nginx', 'andino', 'andino-solr', 'andino-postfix', 'andino-redis', 'andino-db']
    },
    "portal_datos.gob.ar": {
        "containers": [
            'datosgobar-nginx', 'datosgobar', 'datosgobar-solr',
            'datosgobar-postfix', 'datosgobar-redis', 'datosgobar-db',
        ]
    }
}

COMPOSE_FILE_URL = "https://raw.githubusercontent.com/datosgobar/%s/%s/latest.yml" % (args.repo, args.branch)

EXPECTED_CONTAINERS = REPOS[args.repo]['containers']

UPGRADE_DB_COMMAND = "/etc/ckan_init.d/upgrade_db.sh"
REBUILD_SEARCH_COMMAND = "/etc/ckan_init.d/run_rebuild_search.sh"

def ask(question):
    try:
        _ask = raw_input
    except NameError:
        _ask = input
    return _ask("%s\n" % question)

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

def fix_env_file(base_path):
    env_file = ".env"
    env_file_path = path.join(base_path, env_file)
    nginx_var = "NGINX_HOST_PORT"
    datastore_var = "DATASTORE_HOST_PORT"
    maildomain_var = "maildomain"
    with open(env_file_path, "r+a") as env_f:
        content = env_f.read()
        if nginx_var not in content:
            env_f.write("%s=%s\n" % (nginx_var, "80"))
        if datastore_var not in content:
            env_f.write("%s=%s\n" % (datastore_var, "8800"))
        if maildomain_var not in content:
            maildomain = ask("Por favor, ingrese su dominio para envío de emails (e.g.: myportal.com.ar): ")
            real_maildomain = maildomain.strip()
            if not real_maildomain:
                print("Ningun valor fue ingresado, usando valor por defecto: localhost")
                real_maildomain = "localhost"
            env_f.write("%s=%s\n" % (maildomain_var, real_maildomain))


def backup_database(base_path, compose_path):
    db_container = subprocess.check_output(["docker-compose", "-f", compose_path, "ps", "-q", "db"])
    db_container = db_container.decode("utf-8").strip()
    cmd = [
        "docker",
        "exec",
        db_container,
        "bash",
        "-lc",
        "env PGPASSWORD=$POSTGRES_PASSWORD pg_dump --format=custom -U $POSTGRES_USER $POSTGRES_DB",
    ]
    output = subprocess.check_output(cmd)
    dump_name = "%s-ckan.dump" % time.strftime("%d:%m:%Y:%H:%M:%S")
    dump = path.join(base_path, dump_name)
    with open(dump, "wb") as a_file:
        a_file.write(output)


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
    output = subprocess.check_output([
        "docker",
        "ps",
        "-a",
        "--format",
        "'{{.Names}}'"
    ]).decode("utf-8")
    local_containers = [container.strip("'") for container in output.split()]
    for container_name in EXPECTED_CONTAINERS:
        if container_name not in local_containers:
            print("[ ERROR ] El container %s no se encuentra en la aplicación." % container_name)
            print("[ ERROR ] Por favor instale la aplicación primero.")
            raise Exception("[ ERROR ] No se encontró una instalación.")


def post_update_commands(compose_path):
    try:
        subprocess.check_call(
            ["docker-compose",
            "-f",
            compose_path,
            "exec",
            "portal",
            "bash",
            "/etc/ckan_init.d/run_updates.sh"
            ]
        )
    except CalledProcessError as e:
        print("[ INFO ] Error al correr el script 'run_updates.sh'")
        print(e)
    all_plugins = subprocess.check_output(
        ["docker-compose",
         "-f",
         compose_path,
         "exec",
         "portal",
         "grep", "-E", "^ckan.plugins.*", "/etc/ckan/default/production.ini"]
    ).decode("utf-8").strip()
    subprocess.check_call(
        ["docker-compose",
         "-f",
         compose_path,
         "exec",
         "portal",
         "sed", "-i", "s/^ckan\.plugins.*/ckan.plugins = stats/", "/etc/ckan/default/production.ini"]
    )
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "exec",
        "portal",
        UPGRADE_DB_COMMAND,
    ])
    subprocess.check_call(
        ["docker-compose",
         "-f",
         compose_path,
         "exec",
         "portal",
         "sed", "-i", "s/^ckan\.plugins.*/%s/" % all_plugins, "/etc/ckan/default/production.ini"]
    )
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "exec",
        "portal",
        REBUILD_SEARCH_COMMAND,
    ])


def restart_apps(compose_path):
    subprocess.check_call([
        "docker-compose",
        "-f",
        compose_path,
        "restart",
    ])


def restore_cron_jobs(crontab_content):
    try:
        subprocess.check_call('docker exec -it andino crontab -u www-data -l; {}  '
                              '| crontab -u www-data -'.format(crontab_content), shell=True)
    except subprocess.CalledProcessError:
        # Error durante un deploy
        pass


print("[ INFO ] Comprobando que docker esté instalado...")
check_docker()
print("[ INFO ] Comprobando que docker-compose este instalado...")
check_compose()
directory = path.dirname(path.realpath(__file__))
print("[ INFO ] Comprobando instalación previa...")
check_previous_installation(directory)
print("[ INFO ] Descargando archivos necesarios...")
compose_file_path = get_compose_file(directory)
fix_env_file(directory)
print("[ INFO ] Guardando base de datos...")
backup_database(directory, compose_file_path)
print("[ INFO ] Actualizando la aplicación")
try:
    crontab_content = subprocess.check_output('docker exec -it andino crontab -u www-data -l', shell=True).strip()
except subprocess.CalledProcessError:
    # No hay cronjobs para guardar
    crontab_content = ""
reload_application(compose_file_path)
print("[ INFO ] Corriendo comandos post-instalación")
post_update_commands(compose_file_path)
restore_cron_jobs(crontab_content)
print("[ INFO ] Reiniciando")
restart_apps(compose_file_path)
print("[ INFO ] Listo.")
