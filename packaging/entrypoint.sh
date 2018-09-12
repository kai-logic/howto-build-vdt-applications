#!/bin/bash
set -e

export VIDISPINE_URL=$VIDISPINE_IP_PORT/API/
export THE_NAMESERVER=`cat /etc/resolv.conf | grep "nameserver " | awk '{print $2}' | tr '\n' ' '`

if [ "$1" = 'server' ]; then
    sed -i "s|VIDISPINE_IP_PORT|$VIDISPINE_IP_PORT|g" /etc/nginx/sites-enabled/default
    sed -i "s|THE_NAMESERVER|$THE_NAMESERVER|g" /etc/nginx/sites-enabled/default
    if [[ "$VIDISPINE_IP_PORT" == https://* ]]; then
        sed -i "s|http://|https://|g" /etc/nginx/sites-enabled/default
    fi

    shift
    exec supervisord "$@"
fi

exec "$@"
