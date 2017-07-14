#!/usr/bin/env bash
current_dir="$(dirname "$0")"

"$current_dir/init.sh" -e admin@example.com -h localhost:8080 -p ckan -P ckan -d ckan_datastore -D ckan_datastore
