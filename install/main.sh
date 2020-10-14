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

apt-get install -y supervisor python3-dev python3-pip

apt-get install -y python3-smbus || echo "python3-smbus not installed"

# Install the client

pip_cmd='pip3'

$pip_cmd install unicornclient

# Create configuration file

configuration="[DEFAULT]
host = unicorn.amnt.fr
ssl_verify = True
mqtt_host = 10.0.0.12"

configuration_path="/etc/unicornclient"
mkdir -p $configuration_path
echo "$configuration" > $configuration_path/config.ini

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