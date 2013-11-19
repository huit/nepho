#!/usr/bin/env python
# coding: utf-8

from cement.core import controller, hook
from termcolor import colored
from nepho.cli import base


class NephoScopeController(base.NephoBaseController):
    class Meta:
        label = 'scope'
        interface = controller.IController
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'set a cloudlet (and optionally blueprint) scope for future commands'
        usage = "nepho scope <action> [cloudlet] [blueprint]"
        arguments = [
            (['cloudlet'], dict(help="Name of a cloudlet", nargs='?')),
            (['blueprint'], dict(help="Name of a blueprint (optional)", nargs='?')),
        ]

    @controller.expose(aliases=['set'], help="set a scope for future commands or view current scope")
    def default(self):
        new_cn = self.app.pargs.cloudlet
        new_bp = self.app.pargs.blueprint
        old_cn = self.app.nepho_config.get('scope_cloudlet')
        old_bp = self.app.nepho_config.get('scope_blueprint')

        self.app.log.debug('Setting scope to cloudlet: %s, blueprint: %s' % (new_cn, new_bp))

        if new_cn:
            self.app.nepho_config.set('scope_cloudlet', new_cn)
            if new_bp:
                # Only delete the blueprint if cloudlet is being explicitly set
                # (i.e. user isn't just viewing current scope printout)
                self.app.nepho_config.set('scope_blueprint', new_bp)
            else:
                self.app.nepho_config.unset('scope_blueprint')

            if new_cn != old_cn or new_bp != old_bp:
                print "Set default command scope to " + colored(new_cn, "cyan") + " " + colored(new_bp or "", "yellow")
        elif old_cn is None:
            print "Default command scope is unset. Run nepho scope <cloudlet> [blueprint] to set."

    @controller.expose(help="unset current scope", aliases=['clear'])
    def unset(self):
        self.app.log.debug('Unsetting scope.')
        self.app.nepho_config.unset('scope_cloudlet')
        self.app.nepho_config.unset('scope_blueprint')

        print "Default command scope is now unset. Run nepho scope <cloudlet> [blueprint] to set."


def print_scope(app):
    if app.nepho_config.get('scope_cloudlet') is not None:
        print "Using default command scope " + colored(app.nepho_config.get('scope_cloudlet'), "cyan") + " " + colored(app.nepho_config.get('scope_blueprint') or "", "yellow") + "\n"
    else:
        pass
