#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import blueprint
import argparse

class NephoBlueprintController(base.NephoBaseController):
    class Meta:
        label = 'blueprint'
        stacked_on = None
        description = 'list and view individual cloudlet deployment blueprints'
        usage = "nepho blueprint <action> <cloudlet> [blueprint]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['blueprint'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    @controller.expose(help='List all blueprints in a cloudlet')
    def list(self):
        if self.pargs.cloudlet == None:
            print "Usage: nepho blueprint list <cloudlet>"
            exit(1)

        blueprint.list_blueprint(self, self.pargs.cloudlet)

    @controller.expose(help='Describe a blueprint')
    def describe(self):
        if self.pargs.cloudlet == None or self.pargs.blueprint == None:
            print "Usage: nepho blueprint describe <cloudlet> <blueprint>"
            exit(1)

        blueprint.describe_blueprint(self, self.pargs.cloudlet, self.pargs.blueprint)
