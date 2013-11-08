#!/usr/bin/env python
# coding: utf-8

import argparse
from termcolor import colored
from pprint import pprint

import nepho.core.config
from cement.core import controller
from nepho.cli import base
from nepho.core import common, cloudlet, blueprint, config


class NephoConfigController(base.NephoBaseController):
    class Meta:
        label = 'config'
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'list, view and modify config settings'
        usage = "nepho config <action> [key] [value]"
        arguments = [
            (['key'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['value'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.app.config)

    @controller.expose(help='List all config values.')
    def list(self):
        print "-" * 80
        for k in sorted(self.nepho_config.keys()):
            v = self.nepho_config.get(k)
            if isinstance(v, basestring):
                print colored(" %s: " % (k), "yellow"), colored("\"%s\"" % (v), "blue")
            else:
                print colored(" %s: " % (k), "yellow"), colored("%s" % (v), "blue")
        print "-" * 80

    @controller.expose(help='Get a config value')
    def get(self):
        if self.app.pargs.key is None:
            print "Usage: nepho config get <key>"
            exit(1)
        print self.nepho_config.get(self.app.pargs.key)

    @controller.expose(help='Set a config value', aliases=["add"])
    def set(self):
        if self.app.pargs.key is None or self.app.pargs.value is None:
            print "Usage: nepho config set <key> <value>"
            exit(1)
        self.nepho_config.set(self.app.pargs.key, self.app.pargs.value)

    @controller.expose(help='Unset a config value', aliases=["delete", "remove"])
    def unset(self):
        if self.app.pargs.key is None:
            print "Usage: nepho config unset <key>"
            exit(1)
        self.nepho_config.unset(self.app.pargs.key)
