#!/usr/bin/env python
# coding: utf-8
from cement.core import controller
from nepho.cli import base
from os import path
import argparse
from termcolor import colored
from textwrap import TextWrapper

from nepho.core import common, cloudlet


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

    def _setup(self, app):
        super(NephoCloudletController, self)._setup(app)
        self.cloudletManager = cloudlet.CloudletManager(self.config)
        
    @controller.expose(help="List all installed cloudlets")
    def list(self):
        
        cloudlets = self.cloudletManager.list()
        
        #    all_cloudlets = common.all_cloudlets(self)
        dir = ""
        items = list()
        for cloudlet in cloudlets: #sorted(all_cloudlets):
            # Print directory if it changes
            cloudlet_path = cloudlet.get_path()
            if dir != path.dirname(cloudlet_path):
                dir = path.dirname(cloudlet_path)
                print colored(dir, "cyan")
            name = path.basename(cloudlet_path)

            # If there are multiple versions of a cloudlet with the same name,
            # subsequent versions will be ignored by other commands
            if name not in items:
                try:
                    y = cloudlet.defn
                except:
                    print colored("└──", "yellow"), name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
                else:
                    print colored("└──", "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"
                items.append(name)
            else:
                print colored("└──", "yellow"), name, "(", colored("error", "red"), "- duplicate cloudlet will be ignored )"
        return
    
        #cloudlet.list_all_cloudlets(self)

    @controller.expose(help="Describe an installed cloudlet")
    def describe(self):
        self.cloudletManager.find(self.pargs.string[0]).describe()
        #cloudlet.describe_cloudlet(self, self.pargs.string[0])

    @controller.expose(help="Search the Nepho Cloudlet Registry for cloudlets whose names, summaries, or descriptions match the provided search term")
    def search(self):
        # TODO: Improve registry search. I started looking into fulltext search
        # options, and experimented with throwing the registry into a local
        # sqlite database, but it seemed like overkill. Really this should be
        # calling a web service.
        print "Unimplemented action. (input: %s)" % self.pargs.string

    @controller.expose(help="Install a Nepho cloudlet from the Nepho Cloudlet Registry or from an external Git repository")
    def install(self):
        if self.pargs.string == []:
            print "Usage: nepho cloudlet install <cloudlet> [--location <location>]"
            exit(1)

        name = self.pargs.string[0]
        #registry = cloudlet.cloudlet_registry(self)

        if name in self.cloudletManager.get_registry():
            url = registry[name]['source']
        else:
            if self.pargs.location is None:
                print "Cloudlet name was not found in master registry. To install a custom cloudlet, specify a location with the --location option."
                exit(1)
            else:
                url = self.pargs.location

        
        cloudlet_dirs = self.cloudletManager.all_cloudlet_dirs()
        selected_dir = common.select_list(self, cloudlet_dirs, False, "Select an install location:")

        cloudlt = self.cloudletManager.new(name, selected_dir, url)
#        cloudlt.clone(url)
        
#        cloudlet_dirs = self.config.get('nepho', 'cloudlet_dirs')
#        selected_dir = common.select_list(self, cloudlet_dirs, False, "Select an install location:")

#        repo_path = path.join(selected_dir, name)

        # The clone_cloudlet method will validate the location URL
#        cloudlet.clone_cloudlet(self, url, repo_path)

    @controller.expose(help="Upgrade an installed Nepho cloudlet")
    def upgrade(self):
        
        cloudlts = self.cloudletManager.find(self.pargs.string[0])
        if cloudlts is None:
            print "Cloudlet is not installed."
            exit(1)
        
        if not isinstance(cloudlts, list):
            cloudlts = [cloudlts]
        for cloudlt in cloudlts:
            cloudlt.update()

    @controller.expose(help="Uninstall a Nepho cloudlet")
    def uninstall(self):
        name = self.pargs.string[0]
        cloudlt = self.cloudletManager.find(name)
        
        if cloudlt is None:
            print "No cloudlet named %s was found.\n" % (name)
            exit(1)
        if not self.pargs.force:
            verify = input("Are you sure you want to uninstall %s? [y/N]: " % (name))
            if verify != 'y' and verify != 'yes':
                exit(1)
            else:
                print "Note: You can hide this message by using the --force option.\n"

        cloudlt.archive(name, self.config.get('nepho', 'archive_dir'))
        cloudlt.uninstall()
        
#        try:
#            name = self.pargs.string[0]
#            possible_paths = common.find_cloudlet(self, name, True)
#        except:
#            print "Invalid cloudlet name provided."
#            exit(1)
#
#        repo_paths = common.select_list(self, possible_paths, True, "Select which cloudlet to uninstall:")
#
#
#        if isinstance(repo_paths, list):
#            for one_path in repo_paths:
#                cloudlet.archive_cloudlet(self, name, one_path)
#        else:
#            cloudlet.archive_cloudlet(self, name, repo_paths)
