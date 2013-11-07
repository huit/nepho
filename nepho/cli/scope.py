#!/usr/bin/env python
# coding: utf-8

from cement.core import controller
from termcolor import colored
from nepho.cli import base


class NephoScopeController(base.NephoBaseController):
    class Meta:
        label = 'scope'
        stacked_on = None
        description = 'set a cloudlet (and optionally blueprint) scope for future commands'
        usage = "nepho config <action> [key] [value]"
        arguments = [
            (['cloudlet'], dict(help="Name of a cloudlet", nargs='?')),
            (['blueprint'], dict(help="Name of a blueprint (optional)", nargs='?')),
        ]

    @controller.expose(aliases=['set'], help="set a scope for future commands or view current scope")
    def default(self):
        self.log.debug('Setting scope to cloudlet: %s, blueprint: %s' % (self.pargs.cloudlet, self.pargs.blueprint))
        if self.pargs.cloudlet:
            self.nepho_config.set('scope_cloudlet', self.pargs.cloudlet)
            if self.pargs.blueprint:
                # Only delete the blueprint if cloudlet is being explicitly set
                # (i.e. user isn't just viewing current scope printout)
                self.nepho_config.set('scope_blueprint', self.pargs.blueprint)
            else:
                self.nepho_config.unset('scope_blueprint')

        cloudlet = self.nepho_config.get('scope_cloudlet')
        blueprint = self.nepho_config.get('scope_blueprint')

        if cloudlet is None and blueprint is None:
            print "Scope unset.  Run nepho scope <cloudlet> [blueprint] to set."
        else:
            print "Scope is currently " + colored(cloudlet, "blue") + " " + colored(blueprint or "", "cyan")

    @controller.expose(help="unset current scope")
    def unset(self):
        self.log.debug('Unsetting scope.')
        self.nepho_config.unset('scope_cloudlet')
        self.nepho_config.unset('scope_blueprint')

        print "Default scope unset.  Run nepho scope <cloudlet> [blueprint] to set."

    def display(self):
        cloudlet = self.nepho_config.get('scope_cloudlet')
        blueprint = self.nepho_config.get('scope_blueprint')

        if cloudlet is not None:
            print "Default scope is " + colored(cloudlet, "blue") + " " + colored(blueprint or "", "cyan")
