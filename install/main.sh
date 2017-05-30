#!/usr/bin/env bash
set -e
set -x

apt-get update
apt-get upgrade -y

apt-get install htop git
apt-get install rsync supervisor
apt-get install python-dev

curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python get-pip.py

pip install -U pip
pip install unicornhat