#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import scenario
import argparse

class NephoScenarioController(base.NephoBaseController):
    class Meta:
        label = 'scenario'
        stacked_on = None
        description = 'list and view individual cloudlet deployment scenarios'
        usage = "nepho scenario <action> <cloudlet> [scenario]"
        arguments = [
            (['cloudlet'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['scenario'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    @controller.expose(help='List all scenarios in a cloudlet')
    def list(self):
    	if self.pargs.cloudlet == None:
    		print "Usage: nepho scenario list <cloudlet>"
    		exit(1)

    	scenario.list_scenario(self, self.pargs.cloudlet)

    @controller.expose(help='Describe a scenario')
    def describe(self):
    	if self.pargs.cloudlet == None or self.pargs.scenario == None:
            print "Usage: nepho scenario describe <cloudlet> <scenario>"
            exit(1)

        scenario.describe_scenario(self, self.pargs.cloudlet, self.pargs.scenario)