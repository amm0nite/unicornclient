#!/usr/bin/env bash
mkdir -p dist
rm -rv dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
