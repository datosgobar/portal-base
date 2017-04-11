#!/usr/bin/env bash
current_dir="$(dirname "$0")"

"$current_dir/paster.sh" --plugin=ckan db upgrade
