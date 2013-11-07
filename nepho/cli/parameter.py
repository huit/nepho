#!/usr/bin/env python
# coding: utf-8

import argparse
from termcolor import colored
from pprint import pprint

import nepho.core.config
from cement.core import controller
from nepho.cli import base
from nepho.core import common, cloudlet, blueprint, config


class NephoParameterController(base.NephoBaseController):
    class Meta:
        label = 'parameter'
        stacked_on = None
        description = 'list, view and modify parameter settings'
        usage = "nepho parameter <action> [cloudlet] [blueprint] [key] [value]"
        arguments = [
            (['--cloudlet'], dict(dest='cloudlet', help=argparse.SUPPRESS, nargs='?')),
            (['--blueprint'], dict(dest='blueprint', help=argparse.SUPPRESS, nargs='?')),
            (['key'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['value'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.config)

    @controller.expose(help='List parameters.')
    def list(self):

        print "-" * 80

        keys = sorted(self.nepho_config.keys("parameters"))
        for k in keys:
            v = self.nepho_config.get(k, "parameters")
            if isinstance(v, basestring):
                print colored(" %s: " % (k), "yellow"), colored("\"%s\"" % (v), "blue")
            else:
                print colored(" %s: " % (k), "yellow"), colored("%s" % (v), "blue")
        print "-" * 80

    @controller.expose(help='Get a parameter value')
    def get(self):
        if self.pargs.key is None:
            print "Usage: nepho parameter get <key>"
            exit(1)
        domain = "parameters"
        print self.nepho_config.get(self.pargs.key, domain)

    @controller.expose(help='Set a parameter value', aliases=["add"])
    def set(self):
        if self.pargs.key is None or self.pargs.value is None:
            print "Usage: nepho parameter set <key>"
            exit(1)
        domain = "parameters"

        self.nepho_config.set(self.pargs.key, self.pargs.value, domain)

    @controller.expose(help='unset a parameter value', aliases=["remove", "delete"])
    def unset(self):
        if self.pargs.key is None:
            print "Usage: nepho parameter unset <key>"
            exit(1)
        domain = "parameters"

        self.nepho_config.unset(self.pargs.key, domain)
