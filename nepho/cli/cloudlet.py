#!/usr/bin/env python
# coding: utf-8
from cement.core import controller
from nepho.cli import base, scope
import os
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
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'find, download, and manage cloudlets'
        usage = "nepho cloudlet <action> [options]"
        arguments = [
            (['--force', '-f'], dict(action='store_true', dest='force', help=argparse.SUPPRESS)),
            (['--location', '-l'], dict(dest='location', help=argparse.SUPPRESS)),
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['query'], dict(help=argparse.SUPPRESS, nargs='*')),
        ]

    def _setup(self, app):
        super(NephoCloudletController, self)._setup(app)
        self.cloudletManager = cloudlet.CloudletManager(self.app)

    @controller.expose(help="List all installed cloudlets")
    def list(self):
        cloudlets = self.cloudletManager.list()

        dir = ""
        items = list()

        try:
            for cloudlt in cloudlets:  # sorted(all_cloudlets):
                # Print directory if it changes
                cloudlet_path = cloudlt.get_path()
                if dir != os.path.dirname(cloudlet_path):
                    dir = os.path.dirname(cloudlet_path)
                    print colored(dir, "cyan")
                name = os.path.basename(cloudlet_path)

                # If there are multiple versions of a cloudlet with the same name,
                # subsequent versions will be ignored by other commands
                if name not in items:
                    try:
                        y = cloudlt.definition
                    except:
                        print colored(base.DISP_PATH, "yellow"), name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
                    else:
                        print colored(base.DISP_PATH, "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"
                    items.append(name)
                else:
                    print colored(base.DISP_PATH, "yellow"), name, "(", colored("error", "red"), "- duplicate cloudlet will be ignored )"
        except TypeError:
            print colored(base.DISP_PATH, "yellow"), colored("No cloudlets installed.", "blue")

        return

        #cloudlet.list_all_cloudlets(self)

    @controller.expose(help="Describe an installed cloudlet")
    def describe(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho cloudlet describe <cloudlet>"
            exit(1)
        else:
            scope.print_scope(self)

        c = self.cloudletManager.find(self.app.cloudlet_name)
        if c is None:
            print colored("Error:", "red") + "No cloudlet named \"%s\" found." % (self.cloudlet_name)
            exit(1)
        else:
            wrapper = TextWrapper(width=80, subsequent_indent="              ")
            d = c.definition

            print base.DISP_DASH * 80
            print "Name:         %s" % (d['name'])
            print "Version:      %s" % (d['version'])
            print "Author:       %s" % (d['author'])
            print "License:      %s" % (d['license'])
            print wrapper.fill("Summary:      %s" % (d['summary']))
            print wrapper.fill("Description:  %s" % (d['description']))
            print base.DISP_DASH * 80
        return

    @controller.expose(help="Search the Nepho Cloudlet Registry for cloudlets whose names, summaries, or descriptions match the provided search term")
    def search(self):
        # TODO: Improve search beyond basic string matching

        if self.app.pargs.cloudlet is not None:
            query = self.app.pargs.cloudlet + ' ' + ' '.join(self.app.pargs.query)
        else:
            query = ""

        query = query.strip()

        registry = self.cloudletManager.get_registry()

        if query:
            print "Searching for '%s'" % query + ":"
        else:
            print "Listing all cloudlets:"

        matchList = list()
        for cloudletRepo in registry.keys():
            flattenedText = "%s: %s" % (cloudletRepo, registry[cloudletRepo])
            if (query == '') or (query in flattenedText):
                matchList.append(cloudletRepo)

        if len(matchList) == 0:
            print "No matches found."
        else:
            for cloudletRepo in sorted(matchList):
                cloudletDict = registry[cloudletRepo]

                wrapper = TextWrapper(width=80, subsequent_indent="              ")
                print base.DISP_DASH * 80
                print "Name:         %s" % (cloudletRepo)
                print "Version:      %s" % (cloudletDict['version'])
                print "Author:       %s" % (cloudletDict['author'])
                print "License:      %s" % (cloudletDict['license'])
                print wrapper.fill("Summary:      %s" % (cloudletDict['summary']))

    @controller.expose(help="Install a Nepho cloudlet from the Nepho Cloudlet Registry or from an external Git repository")
    def install(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho cloudlet install <cloudlet> [--location <location>]"
            exit(1)
        else:
            scope.print_scope(self)

        name = self.app.cloudlet_name
        registry = self.cloudletManager.get_registry()

        if name in registry:
            url = registry[name]['source']
            if self.app.config.get('nepho', 'cloudlet_clone_proto') == "ssh":
                url = url.replace('https://github.com/', 'git@github.com:', 1)
        else:
            if self.app.pargs.location is None:
                print "Cloudlet name was not found in master registry. To install a custom cloudlet, specify a location with the --location option."
                exit(1)
            else:
                url = self.app.pargs.location

        cloudlet_dirs = self.cloudletManager.all_cloudlet_dirs()
        selected_dir = common.select_list(self, cloudlet_dirs, False, "Select an install location:")

        # TODO: Move error handling from core to CLI
        self.cloudletManager.new(name, selected_dir, url)
        return

    @controller.expose(help="Upgrade an installed Nepho cloudlet", aliases=["upgrade"])
    def update(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho cloudlet update <cloudlet>"
            exit(1)
        else:
            scope.print_scope(self)

        cl = self.cloudletManager.find(self.app.cloudlet_name)
        if cl is None:
            print colored("Error: ", "red") + "Cloudlet is not installed."
            exit(1)

        if not isinstance(cl, list):
            cl = [cl]
        for c in cl:
            try:
                c.update()
            except AssertionError:
                print colored("Error: ", "red") + "Cloudlet update failed, see issue #176."

    @controller.expose(help="Uninstall a Nepho cloudlet", aliases=["remove"])
    def uninstall(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho cloudlet uninstall [--force/-f] <cloudlet>"
            exit(1)
        else:
            scope.print_scope(self)

        cl = self.cloudletManager.find(self.app.cloudlet_name)
        if cl is None:
            print colored("Error: ", "red") + "Cloudlet is not installed."
            exit(1)

        if not self.app.pargs.force:
            verify = input("Are you sure you want to uninstall %s? [y/N]: " % (self.app.cloudlet_name))
            if verify != 'y' and verify != 'yes':
                exit(1)

        if not isinstance(cl, list):
            cl = [cl]
        for c in cl:
            c.archive(self.app.cloudlet_name, self.app.config.get('nepho', 'archive_dir'))
            c.uninstall()

    @controller.expose(help="Update the local cloudlet registry.", aliases=["update-registry"])
    def registry_update(self):
        self.cloudletManager.clear_registry()
        self.cloudletManager.update_registry()
