#!/usr/bin/env python
# coding: utf-8

import argparse
from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint

import nepho.core.config
from cement.core import controller
from nepho.cli import base, scope
from nepho.core import cloudlet


class NephoBlueprintController(base.NephoBaseController):
    class Meta:
        label = 'blueprint'
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'list and view individual cloudlet deployment blueprints'
        usage = "nepho blueprint <action> <cloudlet> [blueprint]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['blueprint'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.app.config)
        self.cloudletManager = cloudlet.CloudletManager(self.nepho_config)

    @controller.expose(help='List all blueprints in a cloudlet')
    def list(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho blueprint list <cloudlet>"
            exit(1)
        else:
            scope.print_scope(self)

        try:
            cloudlt = self.cloudletManager.find(self.app.cloudlet_name)
            y = cloudlt.definition
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        except AttributeError:
            print 'Could not find Cloudlet:'
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"

        blueprints = cloudlt.blueprints()

        # Prepare to wrap description text
        wrapper = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")

        # Now list the available blueprints
        for bp in blueprints:
            if bp.definition is not None:
                print colored("    └──", "yellow"), colored(bp.name, attrs=['underline'])
                print wrapper.fill(y['summary'])
            else:
                print colored("    └──", "yellow"), colored(bp.name, attrs=['underline'])
                print colored("        Error - missing or malformed cloudlet.yaml", "red")

        return

    @controller.expose(help='Describe a blueprint')
    def describe(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho blueprint describe <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        try:
            cloudlt = self.cloudletManager.find(self.app.cloudlet_name)
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            pass
        if cloudlt is None:
            print 'Could not find Cloudlet:'
            exit(1)

        print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (cloudlt.definition['version']), ")"

        bprint = cloudlt.blueprint(self.app.blueprint_name)

        y = bprint.definition

        wrapper = TextWrapper(width=80, subsequent_indent="              ")

        print "-" * 80
        print "name:         %s" % (y['name'])
        print "provider:     %s" % (y['provider'])
        print wrapper.fill("summary:      %s" % (y['summary']))
        print wrapper.fill("description:  %s" % (y['description']))
        print "-" * 80

        p = y.pop('parameters', None)

        pprint(p)

        print "-" * 80
        return
