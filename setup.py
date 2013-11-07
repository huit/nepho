#!/usr/bin/env python

from setuptools import setup

setup(
    name         = 'nepho',
    version      = '0.2.2',
    url          = 'http://github.com/huit/nepho',
    description  = 'Simplified cloud orchestration tool for constructing virtual data centers',
    packages     = ['nepho', 'nepho.core', 'nepho.cli', 'nepho.providers'],
    author       = 'Harvard University Information Technology',
    author_email = 'ithelp@harvard.edu',
    license      = 'MIT',
    scripts      = ['bin/nepho'],
    install_requires = [
        'argparse>=1.2',
        'boto>=2.0',
        'awscli>=1.2.3',
        'Jinja2',
        'PyYAML',
        'cement>=2.0',
        'termcolor',
        'gitpython==0.3.2.RC1',
        'requests>=1.2.3',
        'ply==3.4',
        'python-vagrant==0.4.0'
    ],
)
