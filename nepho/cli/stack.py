#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import yaml
import collections
from termcolor import colored
from textwrap import TextWrapper, dedent
from pydoc import pager

from cement.core import controller

from nepho.cli import base, scope
from nepho.core import common, cloudlet, stack, provider, provider_factory, scenario, parameter


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
            (['--name', '-n'], dict(help='custom stack name (aws only)', default=None)),
            (['--params', '-p'], dict(help=argparse.SUPPRESS, nargs='*', action='append')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.cloudletManager = cloudlet.CloudletManager(self.app)

    @controller.expose(help='Show the context for a stack from a blueprint and configs')
    def show_context(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack show-context <cloudlet> <blueprint> [-n/--name <stack name] [-s/--save] [-p/--params <param>]"
            exit(1)
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()
        c = s.context

        print "Cloudlet:"
        for k in sorted(c['cloudlet']):
            print "  %-18s: %s" % (k, c['cloudlet'][k])
        print "Blueprint:"
        for k in sorted(c['blueprint']):
            print "  %-18s: %s" % (k, c['blueprint'][k])
        print "Parameters:"
        for k in sorted(c['parameters']):
            print "  %-18s: %s" % (k, c['parameters'][k])

    @controller.expose(help='Validate and display the template output for a stack from a blueprint')
    def validate(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack validate <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()

        output  = "-" * 80 + "\n"
        output += s.provider.validate_template(s.template)
        output += "\n" + "-" * 80 + "\n"
        output += s.provider.format_template(s.template)
        pager(output)

    @controller.expose(help='Display the raw template for a stack from a blueprint')
    def show_template(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack show-template <cloudlet> <blueprint>"
            exit(1)
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()

        template_str = self._assemble_scenario().template
        try:
            template_str = s.provider.format_template(template_str)
        except Exception:
            pass

        print template_str

    @controller.expose(help='Create a stack from a blueprint', aliases=['deploy', 'up'])
    def create(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print dedent("""\
                Usage: nepho stack create <cloudlet> <blueprint> [-n/--name <stack name] [-s/--save] [-p/--params <param>]

                -n, --name <stack name>
                  [AWS ONLY] A custom name for your stack rather than nepho-<cloudlet>-<blueprint>.
                  When using this option you must specify name for other stack actions such as
                  connect, destroy, and status or they will not know which stack to act upon.
                -s, --save
                  [NOT IMPLEMENTED] Save command-line (and/or interactive) parameters to an
                  overrides file for use in all future invocations of this command.

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

        s = self._assemble_scenario()
        s.provider.deploy(self.app)

    @controller.expose(help='Check on the status of a stack.')
    def status(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack status <cloudlet> <blueprint> [-n/--name <stack name]"
            exit(1)
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()

        # For now the provider prints this information
        s.provider.status(self.app)

    @controller.expose(help='Gain access to the stack', aliases=['ssh'])
    def access(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack access <cloudlet> <blueprint> [-n/--name <stack name]"
            exit(1)
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()

        s.provider.access(self.app)

    @controller.expose(help='Destroy a stack from a blueprint', aliases=['delete', 'down'])
    def destroy(self):
        if self.app.cloudlet_name is None or self.app.blueprint_name is None:
            print "Usage: nepho stack destroy <cloudlet> <blueprint> [-n/--name <stack name]"
        else:
            scope.print_scope(self)

        s = self._assemble_scenario()
        s.provider.destroy(self.app)

    @controller.expose(help='List running stacks')
    def list(self):
        scope.print_scope(self)

        print "Unimplemented action. (input: %s)" % self.app.pargs.params
        exit(0)

        try:
            cloudlt = self.cloudletManager.find(self.app.cloudlet_name)
            y = cloudlt.definition
        except IOError:
            print colored(base.DISP_PATH, "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored(base.DISP_PATH, "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"

    def _parse_user_params(self):
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

        stored_params = parameter.ParamsManager(self)
        user_params = self._parse_user_params()
        bprint = self._load_blueprint()
        if self.app.pargs.name is not None:
            stack_name = self.app.pargs.name
        else:
            stack_name = '%s-%s' % (self.app.cloudlet_name, self.app.blueprint_name)
        s = scenario.Scenario(bprint, stored_params, user_params, stack_name)

        return s
