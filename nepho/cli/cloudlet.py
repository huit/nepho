#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from os import path
from nepho.core import common, cloudlet
from pprint import pprint
import argparse

# Python 2.x vs 3.x input handling change
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

class NephoCloudletController(base.NephoBaseController):
    class Meta:
        label = 'cloudlet'
        stacked_on = None
        description = 'find, download, and manage cloudlets'
        usage = "nepho cloudlet <action> [options]"
        arguments = [
            (['--force', '-f'], dict(action='store_true', dest='force', help=argparse.SUPPRESS)),
            (['--location', '-l'], dict(dest='location', help=argparse.SUPPRESS)),
            (['string'], dict(help=argparse.SUPPRESS, nargs='*')),
        ]

    @controller.expose(help="List all installed cloudlets")
    def list(self):
        cloudlet.list_all_cloudlets(self)

    @controller.expose(help="Describe an installed cloudlet")
    def describe(self):
        cloudlet.describe_cloudlet(self, self.pargs.string[0])

    @controller.expose(help="Search the Nepho Cloudlet Registry for cloudlets whose names, summaries, or descriptions match the provided search term")
    def search(self):
        # TODO: Improve registry search. I started looking into fulltext search
        # options, and experimented with throwing the registry into a local
        # sqlite database, but it seemed like overkill. Really this should be
        # calling a web service.
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Install a Nepho cloudlet from the Nepho Cloudlet Registry or from an external Git repository")
    def install(self):
        try:
            name = self.pargs.string[0]
        except Exception as e:
            print "Please provide a cloudlet name."
            exit(1)

        registry = cloudlet.cloudlet_registry(self)

        # At this time, just install in the default directory
        cloudlet_dirs = self.config.get('nepho', 'cloudlet_dirs').split(',')
        repo_path = path.join(cloudlet_dirs[0], name)

        if name in registry:
            url = registry[name]['source']
            cloudlet.clone_cloudlet(self, url, repo_path)
        else:
            if not self.pargs.location:
                print "Cloudlet name was not found in master registry."
                print "To specify a custom Git repository location, use the --location/-l switch."
                exit(1)
            else:
                # The clone_cloudlet method will validate the location URL
                cloudlet.clone_cloudlet(self, self.pargs.location, repo_path)

    @controller.expose(help="Upgrade an installed Nepho cloudlet")
    def upgrade(self):
        try:
            name = self.pargs.string[0]
            repo_path = common.find_cloudlet(self, name)
        except:
            print "Cloudlet is not installed."
            exit(1)

        cloudlet.update_cloudlet(self, repo_path)

    @controller.expose(help="Uninstall a Nepho cloudlet")
    def uninstall(self):
        try:
            name = self.pargs.string[0]
            repo_path = common.find_cloudlet(self, name)
        except:
            print "Invalid cloudlet name provided."
            exit(1)

        if not self.pargs.force:
            verify = input("Are you sure you want to uninstall %s? [y/N] " % (name))
            if verify != 'y' and verify != 'yes':
                exit(1)
            else:
                print "Note: You can hide this message by using the --force option.\n"
        cloudlet.archive_cloudlet(self, name, repo_path)
