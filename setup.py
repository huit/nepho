#!/usr/bin/env python

from setuptools import setup

setup(
    name         = 'nepho',
    version      = '0.2.0',
    url          = 'http://github.com/huit/nepho',
    description  = 'Simplified cloud orchestration tool for constructing virtual data centers',
    packages     = ['nepho', 'nepho.aws'],
    author       = 'Harvard University Information Technology',
    author_email = 'ithelp@harvard.edu',
    license      = 'MIT',
    scripts      = ['bin/nepho'],
    package_data = {
      'nepho': [
        'data/scenarios/*',
        ],
      'nepho.aws': [
        'data/patterns/*/*.cf',
        'data/drivers/*.sh'
        ]
      },
    install_requires = [
      'argparse>=1.2',
      'boto>=2.0',
      'awscli>=0.13',
      'Jinja2',
      'PyYAML',
      'cement>=2.0',
      'termcolor',
      'gitpython',
      'requests==1.2.3',
      'ply==3.4'
    ],
  )
