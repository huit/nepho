#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import yaml
import collections
from termcolor import colored
from textwrap import TextWrapper, dedent
from pprint import pprint

from cement.core import controller

import nepho.core.config
from nepho.cli import base, scope
from nepho.core import common, cloudlet, stack, provider, provider_factory, scenario


class NephoStackController(base.NephoBaseController):
    class Meta:
        label = 'stack'
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'create, manage, and destroy stacks built from blueprints'
        usage = "nepho stack <action> [options]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['blueprint'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['--save', '-s'], dict(help=argparse.SUPPRESS, action='store_true')),
            (['--params', '-p'], dict(help=argparse.SUPPRESS, nargs='*', action='append')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.app.config)
        self.cloudletManager = cloudlet.CloudletManager(self.nepho_config)

    @controller.expose(help='Show the context for a stack from a blueprint and configs')
    def show_context(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack show-context <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()
        ctxt = scene.context

        # Use JSON lib to pretty print a sorted version of this ...
        print colored("Context:", "yellow")
        print colored("-" * 80, "yellow")
        print yaml.dump(ctxt, indent=4)
#        print json.dumps(json.loads(json.dumps(ctxt), object_pairs_hook=collections.OrderedDict), indent=2, separators=(',', ': '))

    @controller.expose(help='Show the template output for a stack from a blueprint')
    def show_template(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack show-template <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()
        print scene.template

    @controller.expose(help='Create a stack from a blueprint', aliases=['deploy', 'up'])
    def create(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print dedent("""\
                Usage: nepho stack create <cloudlet> <blueprint> [-s/--save] [-p/--params <param>]

                -s, --save
                  Save command-line (and/or interactive) parameters to an overrides file for
                  use in all future invocations of this command.

                -p, --params
                  Override any parameter from the blueprint template. This option can be passed
                  multiple key=value pairs, and can be called multiple times. If a required
                  parameter is not passed as a command-line option, nepho will interactively
                  prompt for it.

                Examples:
                  nepho stack create my-app development --params AwsAvailZone1=us-east-1a
                  nepho stack create my-app development -s -p Foo=True Bar=False -p Test=Passed""")
            exit(1)
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()
        scene.provider.deploy()

    @controller.expose(help='Check on the status of a stack.')
    def status(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack status <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()

        status = scene.provider.status()
        print json.dumps(status, sort_keys=True, indent=4, separators=(',', ': '))
        exit(0)

        #
        # Report system status
        #
        header_string = "%s/%s" % (self.app.cloudlet_name, self.app.blueprint_name)
        print colored(header_string, "yellow")
        print colored("-" * len(header_string), "yellow")
        rep_string = "The stack is currently %s." % (status['default'])
        color = "blue"
        if status['default'] == "running":
            color = 'green'
        if status['default'] == "aborted":
            color = 'red'
        print colored(rep_string, color)

    @controller.expose(help='Gain access to the stack', aliases=['ssh'])
    def access(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack access <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()

        scene.provider.access()

    @controller.expose(help='Destroy a stack from a blueprint', aliases=['delete'])
    def destroy(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack destroy <cloudlet> <blueprint>"
        else:
            scope.print_scope(self)

        scene = self._assemble_scenario()
        scene.provider.destroy()

    @controller.expose(help='List running stacks')
    def list(self):
        scope.print_scope(self)

        try:
            cloudlt = self.cloudletManager.find(self.app.cloudlet_name)
            y = cloudlt.definition
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"

        #bprint = cloudlt.blueprint(self.app.blueprint_name)

        # Create an appropriate provider, and set the target pattern.
        #provider_name = bprint.provider_name
        #providr = provider.ProviderFactory(provider_name, self.app.config)
        #providr.pattern(bprint.pattern())

        print "Partially implemented action. (input: %s)" % self.app.pargs.params

    def _parse_params(self):
        """Helper method to extract params from command line into a dict."""
        params = dict()
        if self.app.pargs.params is not None:
            paramList = self.app.pargs.params
            for item in paramList[0]:
                (k, v) = item.split("=")
                params[k] = v
        return params

    def _load_blueprint(self):
        """Helper method to load blueprint & pattern from args."""

        try:
            cloudlt = self.cloudletManager.find(self.app.cloudlet_name)
        except Exception:
            print colored("Error loading cloudlet %s" % (self.app.cloudlet_name), "red")
            exit(1)

        bprint = cloudlt.blueprint(self.app.blueprint_name)

        if bprint is None:
            print "Cannot find blueprint %s in cloudlet %s." % (self.app.blueprint_name, self.app.cloudlet_name)
            exit(1)

        return bprint

    def _assemble_scenario(self):
        """Helper method to create a suitable scenario from the command line options."""

        params = self._parse_params()
        bprint = self._load_blueprint()
        scene = scenario.Scenario(self.nepho_config, bprint, params)

        return scene
