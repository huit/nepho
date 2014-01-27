#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint

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
        self.cloudletManager = cloudlet.CloudletManager(self.app)

    @controller.expose(help='List all blueprints in a cloudlet')
    def list(self):
        if self.app.cloudlet_name is None:
            print "Usage: nepho blueprint list <cloudlet>"
            exit(1)
        else:
            scope.print_scope(self)

        c = _load_cloudlet(self, self.app.cloudlet_name)
        blueprints = c.blueprints()

        # Prepare to wrap description text
        wrapper = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")

        # Now list the available blueprints
        for bp in blueprints:
            if bp.definition is not None:
                print colored("    " + base.DISP_PATH, "yellow"), colored(bp.name, attrs=['underline']), "[", colored(bp.definition['provider'], 'magenta'), "]"
                print wrapper.fill(bp.definition['summary'])
            else:
                print colored("    " + base.DISP_PATH, "yellow"), colored(bp.name, attrs=['underline'])
                print colored("        Error - missing or malformed blueprint.yaml", "red")

        return

    @controller.expose(help='Describe a blueprint')
    def describe(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho blueprint describe <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        c = _load_cloudlet(self, self.app.cloudlet_name)
        bp = c.blueprint(self.app.blueprint_name)

        if bp is None:
            print colored("Error: ", "red"), "No blueprint by that name.\nFor a list of blueprints run `nepho blueprint list %s`" % (self.app.cloudlet_name)
            exit(1)

        wrapper  = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")
        wrapper2 = TextWrapper(width=80, initial_indent="          ", subsequent_indent="          ")

        if bp.definition is not None:
            print colored("    " + base.DISP_PATH, "yellow"), colored(bp.name, attrs=['underline']), "[", colored(bp.definition['provider'], 'magenta'), "]"
            print wrapper.fill(bp.definition['summary'])
        else:
            print colored("    " + base.DISP_PATH, "yellow"), colored(bp.name, attrs=['underline'])
            print colored("        Error - missing or malformed blueprint.yaml", "red")
            return

        print "\n        Description:"
        print wrapper2.fill(bp.definition['description'])

        print "\n        Default Parameters:"
        params = bp.definition.pop('parameters', None)
        for k, v in params.iteritems():
            print "          %-18s: %s" % (k, v)
        print
        return


def _load_cloudlet(app_obj, name):
    try:
        c = app_obj.cloudletManager.find(name)
    except IOError:
        print colored("Error: ", "red"), "Missing or malformed cloudlet.yaml for %s" % (c.name)
        exit(1)

    if c is None:
        print colored("Error: ", "red"), "Could not find cloudlet %s.\nFor a list of cloudlets run `nepho cloudlet list`" % (name)
        exit(1)

    print colored(os.path.dirname(c.get_path()), "cyan")
    print colored(base.DISP_PATH, "yellow"), c.name, "(", colored("v%s", "blue") % (c.definition['version']), ")"
    return c
