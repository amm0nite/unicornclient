#!/usr/bin/env bash
rm -rv dist
python setup.py sdist
twine upload dist/*
