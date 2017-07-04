msgcat --use-first \
    "$1" \
    "/usr/lib/ckan/default/src/ckan/ckan/i18n/es/LC_MESSAGES/ckan.po" \
| msgfmt - -o "/usr/lib/ckan/default/src/ckan/ckan/i18n/es/LC_MESSAGES/ckan.mo"
