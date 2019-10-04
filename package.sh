#!/usr/bin/env bash
mkdir -p dist
rm -rv dist
python3 setup.py sdist
twine upload dist/*
