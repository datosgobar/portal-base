#!/usr/bin/env bash
current_dir="$(dirname "$0")"
usage() {
	echo "Usage: `basename $0`" >&2
	echo "(-u datapusher_host)" >&2
	echo "(-e error_email_from)" >&2
	echo "(-h site_host or ip)" >&2
	echo "(-p database_user) (-p database_password)" >&2
	echo "(-d datastore_user) (-D datastore_password)" >&2
}
if ( ! getopts "u:e:h:p:P:d:D:" opt); then
    usage;
	exit $E_OPTERROR;
fi

while getopts "u:e:h:p:P:d:D:" opt;do
	case "$opt" in
	u)
	  datapusher_host="$OPTARG"
      ;;
	e)
	  error_email="$OPTARG"
      ;;
	h)
	  site_host="$OPTARG"
      ;;
	p)
	  database_user="$OPTARG"
      ;;
	P)
	  database_password="$OPTARG"
      ;;
	d)
	  datastore_user="$OPTARG"
      ;;
	D)
	  datastore_password="$OPTARG"
      ;;
	\?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
	esac
done

export PGHOST=db
export PGPORT=5432
export PGDATABASE=ckan
export DATASTORE_DB=datastore_default

"$current_dir/change_datapusher_url.sh" "http://$datapusher_host:8800"
"$current_dir/update_conf.sh" "error_email_from=$error_email"
"$current_dir/change_site_url.sh" "http://$site_host"
"$current_dir/update_conf.sh" "sqlalchemy.url=postgresql://$database_user:$database_password@$PGHOST:$PGPORT/$PGDATABASE"
"$current_dir/update_conf.sh" "ckan.datastore.write_url=postgresql://$database_user:$database_password@$PGHOST:$PGPORT/$DATASTORE_DB"
"$current_dir/update_conf.sh" "ckan.datastore.read_url=postgresql://$datastore_user:$datastore_password@$PGHOST:$PGPORT/$DATASTORE_DB"
# Create datastore role and database

"$current_dir/paster.sh" --plugin=ckan db init
export PGUSER="$database_user"
export PGPASSWORD="$database_password"
psql -c "CREATE ROLE $datastore_user WITH PASSWORD '$datastore_password';"
psql -c "CREATE DATABASE $DATASTORE_DB OWNER $database_user;"
"$current_dir/paster.sh" --plugin=ckan datastore set-permissions| psql --set ON_ERROR_STOP=1
"$current_dir/paster.sh" --plugin=ckanext-harvest harvester initdb
