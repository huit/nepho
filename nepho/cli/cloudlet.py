#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import cloudlet
import argparse

class NephoCloudletController(base.NephoBaseController):
    class Meta:
        label = 'cloudlet'
        stacked_on = None
        description = 'find, download, and manage cloudlets'
        usage = "nepho cloudlet <action> [options]"
        arguments = [
            (['string'], dict(help=argparse.SUPPRESS, nargs='*')),
        ]

    @controller.expose(help="List all installed cloudlets")
    def list(self):
    	cloudlet.list_all(self)

    @controller.expose(help="Search the Nepho Cloudlet Registry for cloudlets whose names, summaries, or descriptions match the provided search term")
    def search(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Install a Nepho cloudlet from the Nepho Cloudlet Registry or from an external Git repository")
    def install(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Upgrade an installed Nepho cloudlet")
    def upgrade(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Uninstall a Nepho cloudlet")
    def uninstall(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string