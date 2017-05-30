#!/usr/bin/env bash
export PYTHONENV='prod'
python -u -m unicorn_client.client
