#!/usr/bin/env python
# coding: utf-8

import argparse
from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint

import nepho.core.config
from cement.core import controller
from nepho.cli import base
from nepho.core import common, cloudlet, blueprint, config

class NephoConfigController(base.NephoBaseController):
    class Meta:
        label = 'config'
        stacked_on = None
        description = 'list, view and modify config settings'
        usage = "nepho config <action> <cloudlet> [blueprint]"
        arguments = [
            (['key'], dict(help=argparse.SUPPRESS, nargs='?')),
            (['value'], dict(help=argparse.SUPPRESS, nargs='?')),
        ]

    def _setup(self, app):
        super(base.NephoBaseController, self)._setup(app)
        self.nepho_config = nepho.core.config.ConfigManager(self.config)
        
    @controller.expose(help='List all blueprints in a cloudlet')
    def list(self):

        # Prepare to wrap description text
        wrapper = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")
        print "-" * 80
                
        keys = sorted(self.nepho_config.keys( ) )
        for k in keys:
            v = self.nepho_config.get(k)
            if isinstance(v, basestring):
                print colored(" %s: " % (k), "yellow" ), colored( "\"%s\"" % (v), "blue" )
            else:
                print colored(" %s: " % (k), "yellow" ), colored( "%s" % (v), "blue"  )            
        print "-" * 80

    @controller.expose(help='Get a config value')
    def get(self):
        if self.pargs.key is None:
            print "Usage: nepho config get <key>"
            exit(1)
        print self.nepho_config.get(self.pargs.key)
            
    
    @controller.expose(help='Set a config value')
    def set(self):
        if self.pargs.key is None or self.pargs.value is None:
            print "Usage: nepho config get <key>"
            exit(1)
        self.nepho_config.set(self.pargs.key, self.pargs.value) 
            
    