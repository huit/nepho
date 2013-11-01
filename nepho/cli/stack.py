#!/usr/bin/env python
# coding: utf-8
import argparse
from textwrap import dedent
from cement.core import controller

import nepho.core.config
from nepho.cli import base
from nepho.core import stack


 

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
        
    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.config)
        self.cloudletManager = cloudlet.CloudletManager(self.nepho_config)
 
    @controller.expose(help='Create a stack from a blueprint')
    def deploy(self):
        self.create()
        
                
    @controller.expose(help='Create a stack from a blueprint', aliases=['deploy'])
    def create(self):
        if self.pargs.cloudlet is None or self.pargs.blueprint is None:
            print dedent("""\
                Usage: nepho stack create <cloudlet> <blueprint> [--save] [--params Key1=Val1]

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
                  nepho stack create my-app development -s -p Foo=True -p Bar=False""")
            exit(1)
        try:
            cloudlt = self.cloudletManager.find(self.pargs.cloudlet) 
            y = cloudlt.defn
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"
                    
        bprint = cloudlt.blueprint(self.pargs.blueprint)   
        
        # Create an appropriate provider, and set the target pattern.
        provider_name = bprint.provider_name()
        providr = provider.ProviderFactory(provider_name, self.config)
        providr.pattern(bprint.pattern())
        
        # Do it.
        provider.deploy()
        
        print "Partially implemented action. (input: %s)" % self.pargs.params

    @controller.expose(help='List deployed stacks')
    def list(self):
        if self.pargs.cloudlet is None or self.pargs.blueprint is None:
            print dedent("""
                Usage: nepho stack list <cloudlet> <blueprint> 

                Examples:
                  nepho stack list
                  nepho stack list my-app 
                  nepho stack list my-app development """)
            exit(1)
            
        try:
            cloudlt = self.cloudletManager.find(self.pargs.cloudlet) 
            y = cloudlt.defn
        except IOError:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            exit(1)
        else:
            print colored("└──", "yellow"), cloudlt.name, "(", colored("v%s", "blue") % (y['version']), ")"
                    
        bprint = cloudlt.blueprint(self.pargs.blueprint)   
        
        # Create an appropriate provider, and set the target pattern.
        provider_name = bprint.provider_name()
        providr = provider.ProviderFactory(provider_name, self.config)
        providr.pattern(bprint.pattern())
        
        # Do it.
        provider.deploy()
        
        print "Partially implemented action. (input: %s)" % self.pargs.params
