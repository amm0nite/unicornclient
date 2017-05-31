#!/usr/bin/env bash
set -e
set -x

apt-get update
apt-get upgrade -y

apt-get install htop git curl rsync
apt-get install python-dev supervisor

curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python get-pip.py

pip install -U pip
pip install unicornhat