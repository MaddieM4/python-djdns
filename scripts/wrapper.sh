#!/bin/bash

set -e

uname="djdns"
script_dir="`dirname $0`"
repo_dir="$script_dir/.."
venv_dir=/var/dns/venv
data_dir=/var/dns/data

# WRAPPER : Run djdns from the virtualenv, in the console.
# Useful for debugging when djdns refuses to start.

# It mostly works like sysvrc, except with -v on.

if [[ -d "$venv_dir" ]]; then
    echo "Activating into virtualenv $venv_dir"
    source "$venv_dir/bin/activate"
else
    echo "Could not find virtualenv $venv_dir, plowing ahead"
fi

echo "Starting djdns..."
djdns -d "$data_dir" -u $uname -v
