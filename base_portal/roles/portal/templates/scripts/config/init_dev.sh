#!/usr/bin/env bash
current_dir="$(dirname "$0")"

"$current_dir/init.sh" -e admin@example.com -h localhost -p ckan -P ckan -d ckan_datastore -D ckan_datastore
