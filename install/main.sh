#!/usr/bin/env bash
set -e
set -x

# RASPBIAN INSTALL SCRIPT

if [[ $EUID -ne 0 ]]
then
   echo "Please run as root"
   exit 1
fi

apt-get update

apt-get install -y htop git rsync
apt-get install -y python-dev supervisor

pip_cmd='pip2.7'

pip_test=0
command -v $pip_cmd || pip_test=1

if [[ $pip_test -ne 0 ]]
then
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
    python get-pip.py
    rm get-pip.py
fi

$pip_cmd install -U pip
$pip_cmd install unicornclient

start_script="#!/usr/bin/env bash
pip install -U unicornclient
export PYTHONUNBUFFERED=1
exec unicornclient"

echo "$start_script" > /root/unicornclient.sh
chmod u+x /root/unicornclient.sh

supervisor_configuration="[program:unicornclient]
user=root
directory=/root
command=bash -c ""/root/unicornclient.sh""
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/dev/shm/unicornclient.log
stopsignal=KILL
stopasgroup=true"

supervisor_path="/etc/supervisor/conf.d/"
if [ -d "$supervisor_path" ]; then
    echo "$supervisor_configuration" > $supervisor_path/unicornclient.conf
    supervisorctl update
fi