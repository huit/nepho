#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import cloudlet
from pprint import pprint
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
        cloudlet.list_all_cloudlets(self)

    @controller.expose(help="Describe an installed cloudlet")
    def describe(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Search the Nepho Cloudlet Registry for cloudlets whose names, summaries, or descriptions match the provided search term")
    def search(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Install a Nepho cloudlet from the Nepho Cloudlet Registry or from an external Git repository")
    def install(self):
        registry = cloudlet.cloudlet_registry(self)
        input = self.pargs.string[0]
        if input in registry:
            print "Found cloudlet in registry"
        #       download from git url in registry
        else:
            print "Cloudlet not in registry"
        #       validate git url
        #           if valid
        #               download from git url
        #           if not valid
        #               throw error
        # download submodules as well
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Upgrade an installed Nepho cloudlet")
    def upgrade(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Uninstall a Nepho cloudlet")
    def uninstall(self):
        print "Unimplemented action. (input: %s)" % self.pargs.string
