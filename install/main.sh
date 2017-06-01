#!/usr/bin/env bash
set -e
set -x

if [[ $EUID -ne 0 ]]
then
   echo "Please run as root"
   exit 1
fi

apt-get update

apt-get install -y htop git curl rsync
apt-get install -y python-dev supervisor

pip_test=0
command -v pip || pip_test=1

if [[ $pip_test -ne 0 ]]
then
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
    python get-pip.py
fi

pip install -U pip
pip install unicornclient

supervisor_configuration="[program:unicornclient]
user=root
directory=/root
command=unicornclient
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/dev/shm/unicornclient.log
stopsignal=KILL
stopasgroup=true"

supervisor_path="/etc/supervisor/conf.d/"
if [ -d "$supervisor_path" ]; then
    echo "$supervisor_configuration" > $supervisor_path/unicornclient.conf
fi