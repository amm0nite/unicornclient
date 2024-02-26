#!/usr/bin/env python
# pylint: disable=exec-used,undefined-variable

from setuptools import setup, find_packages
from unicornclient.version import VERSION

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name             = 'unicornclient',
    version          = VERSION,
    author           = 'Pierre Cavan',
    author_email     = 'ammonite.myfox@gmail.com',
    description      = """Unicorn client""",
    long_description = """Unicorn client""",
    license          = 'MIT',
    keywords         = 'Raspberry Pi',
    url              = 'https://github.com/amm0nite/unicornclient',
    classifiers      = CLASSIFIERS,
    packages         = find_packages(),
    install_requires = read_requirements(),
    entry_points     = {'console_scripts': ['unicornclient=unicornclient.agent:main']}
)


# https://packaging.python.org/
# http://peterdowns.com/posts/first-time-with-pypi.html
# https://github.com/pimoroni/unicorn-hat/tree/master/library/UnicornHat
# https://github.com/pypa/sampleproject
# TL;DR https://stackoverflow.com/a/42489974
