#!/bin/bash

set -e

script_dir="`dirname $0`"
repo_dir="$script_dir/.."
venv_dir=/var/dns/venv
data_dir=/var/dns/data

function update_djdns {
    echo "Updating DJDNS..."
    . "$venv_dir/bin/activate"
    cd "$repo_dir"
    pip install --upgrade -r requirements.txt
    yes | pip uninstall djdns
    python setup.py install
    deactivate

    cp "$script_dir/wrapper.sh" /usr/bin/djdns
    cp "$script_dir/sysvrc" /etc/init.d/djdns
}

function update_source_data {
    echo "Updating source data..."
    cd "$data_dir"
    git pull
}

update_djdns
update_source_data
/etc/init.d/djdns restart
