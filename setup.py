#!/usr/bin/env python

from setuptools import setup
import os

# Markdown to ReStructuredText conversion
long_description = 'Nepho is a command-line tool that orchestrates the creation of complete working application stacks on virtual infrastructure. Initially targeting Amazon Web Services as well as Vagrant, Nepho abstracts datacenter creation, instance configuration, and application deployment into portable "cloudlets" that can be shared between developers and teams.'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()


setup(
    name         = 'nepho',
    version      = '1.1.0',
    url          = 'http://github.com/huit/nepho',
    description  = 'Simplified cloud orchestration tool for constructing virtual data centers',
    long_description = long_description,
    packages     = ['nepho', 'nepho.core', 'nepho.cli', 'nepho.providers'],
    author       = 'Harvard University Information Technology',
    author_email = 'ithelp@harvard.edu',
    license      = 'LICENSE.txt',
    entry_points = {
        'console_scripts': [
            'nepho=nepho.cli.bootstrap:run',
        ]
    },
    dependency_links = [
        'git+git://github.com/cement/cement.git@2.1.4.dev20131029203905#egg=cement-2.1.4-dev'
    ],
    install_requires = [
        'argparse>=1.2',
        'boto>=2.0',
        'Jinja2',
        'PyYAML',
        'cement>=2.1,==2.1.4-dev',
        'termcolor',
        'colorama',
        'gitpython==0.3.2.RC1',
        'requests>=1.2.3',
        'python-vagrant==0.4.0'
    ],
    setup_requires = [
        'setuptools_git>=1.0',
        'pypandoc>=0.7.0',
    ],
    test_suite = 'nose.collector',
    tests_require = [
        'flake8>=2.1.0',
        'nose>=1.3.0',
        'coverage>=3.7',
    ],
)
