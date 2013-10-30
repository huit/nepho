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
        if self.pargs.cloudlet is None:
            print "Usage: nepho blueprint list <cloudlet>"
            exit(1)

        cloudlet = CloudletManager.retrieve(self.pargs.cloudlet) 
        blueprints = cloudlet.getBlueprints()
           
#        blueprint.list_blueprint(self, self.pargs.cloudlet)

    @controller.expose(help='Describe a blueprint')
    def describe(self):
        if self.pargs.cloudlet is None or self.pargs.blueprint is None:
            print "Usage: nepho blueprint describe <cloudlet> <blueprint>"
            exit(1)

        bprint = BlueprintManager.retrieve(self.pargs.cloudlet, self.pargs.blueprint)
        
        blueprint.describe_blueprint(self, self.pargs.cloudlet, self.pargs.blueprint)
