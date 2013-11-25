#!/usr/bin/env python
# coding: utf-8

import argparse
from termcolor import colored
from pprint import pprint

from cement.core import controller
from nepho.cli import base
from nepho.core import common, cloudlet, blueprint, parameter


class NephoParameterController(base.NephoBaseController):
    class Meta:
        label = 'parameter'
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
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
        self.params = parameter.ParamsManager(self)

    @controller.expose(help='List parameters')
    def list(self):
        p = self.params.to_dict()
        print "Global Parameters:"
        for k in sorted(p):
            print "  %-18s: %s" % (k, p[k])

    @controller.expose(help='Get a parameter value')
    def get(self):
        if self.app.pargs.key is None:
            print "Usage: nepho parameter get <key>"
            exit(1)
        else:
            print self.params.get(self.app.pargs.key)

    @controller.expose(help='Set a parameter value', aliases=["add"])
    def set(self):
        if self.app.pargs.key is None or self.app.pargs.value is None:
            print "Usage: nepho parameter set <key> <value>"
            exit(1)
        else:
            self.params.set(self.app.pargs.key, self.app.pargs.value)

    @controller.expose(help='unset a parameter value', aliases=["remove", "delete"])
    def unset(self):
        if self.app.pargs.key is None:
            print "Usage: nepho parameter unset <key>"
            exit(1)
        else:
            self.params.unset(self.app.pargs.key)
