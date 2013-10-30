#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import stack
from textwrap import dedent
import argparse


class NephoStackController(base.NephoBaseController):
    class Meta:
        label = 'stack'
        stacked_on = None
        description = 'create, manage, and destroy stacks built from blueprints'
        usage = "nepho stack <action> [options]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['blueprint'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['--save', '-s'], dict(help=argparse.SUPPRESS, action='store_true')),
            (['--params', '-p'], dict(help=argparse.SUPPRESS, nargs='*', action='append')),
        ]

    @controller.expose(help='Create a stack from a blueprint')
    def create(self):
        if self.pargs.cloudlet is None or self.pargs.blueprint is None:
            print dedent("""\
                Usage: nepho stack create <cloudlet> <blueprint> [--save] [--params Key1=Val1]

                -s, --save
                  Save command-line (and/or interactive) parameters to an overrides file for
                  use in all future invocations of this command.

                -p, --params
                  Override any paramater from the blueprint template. This option can be passed
                  multiple key=value pairs, and can be called multiple times. If a required
                  parameter is not passed as a command-line option, nepho will interactively
                  prompt for it.

                Examples:
                  nepho stack create my-app development --params AwsAvailZone1=us-east-1a
                  nepho stack create my-app development -s -p Foo=True -p Bar=False""")
            exit(1)

        print "Unimplemented action. (input: %s)" % self.pargs.params
