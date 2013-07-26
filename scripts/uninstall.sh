#!/bin/bash

set -e

uname="djdns"
script_dir="`dirname $0`"
repo_dir="$script_dir/.."
venv_dir=/var/dns/venv
data_dir=/var/dns/data

/etc/init.d/djdns stop && true
rm -r "$venv_dir" "$data_dir"
rm /etc/init.d/djdns
update-rc.d -f djdns remove
