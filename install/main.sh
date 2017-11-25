#!/usr/bin/env bash
set -e

# RASPBIAN INSTALL SCRIPT

if [[ $EUID -ne 0 ]]
then
   echo "Please run as root"
   exit 1
fi

# Install package dependencies

apt-get update

apt-get install -y supervisor

apt-get install -y python3-smbus || echo "python3-smbus not installed"

# Update or install pip

pip_cmd='pip3'

pip_test=0
command -v $pip_cmd || pip_test=1

if [[ $pip_test -ne 0 ]]
then
    apt-get install -y python3-dev
    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

$pip_cmd install -U pip

# Install the client

$pip_cmd install unicornclient

# Create start script

start_script="#!/usr/bin/env bash
$pip_cmd install -U unicornclient
export PYTHONUNBUFFERED=1
exec unicornclient"

echo "$start_script" > /root/unicornclient.sh
chmod u+x /root/unicornclient.sh

# Install supervisor program

supervisor_configuration="[program:unicornclient]
user=root
directory=/root
command=bash -c ""/root/unicornclient.sh""
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/dev/shm/unicornclient.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=2
stopsignal=KILL
stopasgroup=true"

supervisor_path="/etc/supervisor/conf.d/"
if [ -d "$supervisor_path" ]; then
    echo "$supervisor_configuration" > $supervisor_path/unicornclient.conf
    supervisorctl update || echo "supervisor not updated"
fi

cron_reboot="0 0 * * 1 root /sbin/reboot"
echo "$cron_reboot" > /etc/cron.d/unicornclient