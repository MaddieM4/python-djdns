#!/bin/bash

set -e

uname="djdns"
script_dir="`dirname $0`"
repo_dir="$script_dir/.."
venv_dir=/var/dns/venv
data_dir=/var/dns/data

function user_exists {
    if id "$1" > /dev/null 2>&1; then
        echo "true";
    else
        echo "false";
    fi;
}

function create_user {
    # Generate depriveleged user for daemon
    local uname=$1
    local shell=`which nologin`

    useradd -s $shell --system --home /var/dns $uname
}

function setup_user {
    echo -n "Does user $uname exist... "
    local exists=$(user_exists $uname)
    echo "$exists"
    case $exists in
        true)   echo "user $uname exists";;
        false)  echo "user $uname does not exist, creating...";
                create_user $uname;;
        *) echo "Failure. WTF."; exit 1;;
    esac
}

function setup_initscript {
    cp "$script_dir/wrapper.sh" /usr/bin/djdns
    cp "$script_dir/sysvrc" /etc/init.d/djdns
    update-rc.d djdns start 20 2 3 4 5 . stop 20 0 1 6 .
}

function setup_virtualenv {
    if [[ -d $venv_dir ]]; then
        echo "Not creating $venv_dir, already exists"
        return
    fi;
    echo "Creating $venv_dir"

    mkdir -p /var/dns/
    virtualenv $venv_dir

    . $venv_dir/bin/activate
    pip install -r $repo_dir/requirements.txt
    if python --version 2>&1 | grep ' 2.6'; then
        pip install unittest2
    fi
    cd $repo_dir
    python setup.py install
    deactivate
}

function setup_data {
    local repo="https://github.com/campadrenalin/djdns-hype-flat.git"
    if [[ -d $data_dir ]]; then
        echo "Not creating $data_dir, already exists"
        return
    fi;
    echo "Creating $data_dir"

    mkdir -p /var/dns/

    git clone $repo $data_dir
}

setup_user
setup_virtualenv
setup_data

chown -R $uname:$uname /var/dns/
setup_initscript
/etc/init.d/djdns start
