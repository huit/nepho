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
        stacked_on = None
        description = 'list and view individual cloudlet deployment blueprints'
        usage = "nepho blueprint <action> <cloudlet> [blueprint]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, default=None)),
            (['blueprint'], dict(help=argparse.SUPPRESS, default=None)),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.config)
        self.cloudletManager = cloudlet.CloudletManager(self.nepho_config)

    @controller.expose(help='List all blueprints in a cloudlet')
    def list(self):
        if self.pargs.cloudlet is None:
            print "Usage: nepho blueprint list <cloudlet>"
            exit(1)

        try:
            cloudlt = self.cloudletManager.find(self.pargs.cloudlet)
            y = cloudlt.defn
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"

        blueprints = cloudlt.blueprints()

        # Prepare to wrap description text
        wrapper = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")

        # Now list the available blueprints
        for bp in blueprints:
            if bp.defn is not None:
                print colored("    └──", "yellow"), colored(bp.name, attrs=['underline'])
                print wrapper.fill(y['summary'])
            else:
                print colored("    └──", "yellow"), colored(bp.name, attrs=['underline'])
                print colored("        Error - missing or malformed cloudlet.yaml", "red")

        return

    @controller.expose(help='Describe a blueprint')
    def describe(self):
        if self.pargs.cloudlet is None or self.pargs.blueprint is None:
            print "Usage: nepho blueprint describe <cloudlet> <blueprint>"
            exit(1)

        try:
            cloudlt = self.cloudletManager.find(self.pargs.cloudlet)
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (cloudlt.defn['version']), ")"

        bprint = cloudlt.blueprint(self.pargs.blueprint)
        #bprint = BlueprintManager.retrieve(self.pargs.cloudlet, self.pargs.blueprint)

        #blueprint.describe_blueprint(self, self.pargs.cloudlet, self.pargs.blueprint)

        #y = load_blueprint(self,cloudlet, name)
        y = bprint.defn

        wrapper = TextWrapper(width=80, subsequent_indent="              ")

        print "-" * 80
        print "name:         %s" % (y['name'])
        print "provider:     %s" % (y['provider'])
        print "pattern:      %s" % (y['pattern'])
        print wrapper.fill("summary:      %s" % (y['summary']))
        print wrapper.fill("description:  %s" % (y['description']))
        print "-" * 80

        p = y.pop('parameters', None)

        pprint(p)

        print "-" * 80
        return
