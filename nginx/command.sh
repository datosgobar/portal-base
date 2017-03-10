set -e;
: ${CKAN_HOST:=portal};
NGINX_CONF=/etc/nginx/conf.d/default.conf;
cat /etc/nginx/conf.d/andino.template > $NGINX_CONF;

echo "Using host: $CKAN_HOST";
sed -i.bak s/CKAN_HOST/$CKAN_HOST/g $NGINX_CONF;

echo "Stating nginx...";
nginx -g 'daemon off;'
