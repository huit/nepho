#!/usr/bin/env python

from setuptools import setup

setup(
    name         = 'nepho',
    version      = '0.1.0',
    url          = 'http://github.com/huit/nepho',
    description  = 'Simplified cloud orchestration tool for constructing virtual data centers',
    packages     = ['nepho', 'nepho.aws'],
    author       = 'Harvard University Information Technology',
    author_email = 'ithelp@harvard.edu',
    license      = 'MIT',
    scripts      = ['bin/nepho'],
    package_data = {
      'nepho': [
        'data/deployments/*.yaml',
        'data/deployments/scripts/*.sh'
        ],
      'nepho.aws': [
        'data/patterns/*/*.cf',
        'data/drivers/*.sh'
        ]
      },
    install_requires = ]
      'argparse>=1.2',
      'boto>=2.0',
      'awscli>=0.13',
      'Jinja2',
      'PyYAML'
    ],
  )
