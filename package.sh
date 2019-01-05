#!/usr/bin/env bash
mkdir -p dist
rm -rv dist
python setup.py sdist
twine upload dist/*
