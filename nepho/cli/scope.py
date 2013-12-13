#!/usr/bin/env python
# coding: utf-8

import os
from copy import copy

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
        old_cn = self.app.config.get('scope', 'cloudlet')
        old_bp = self.app.config.get('scope', 'blueprint')

        self.app.log.debug('Setting scope to cloudlet: %s, blueprint: %s' % (new_cn, new_bp))

        if new_cn:
            self.app.config.set('scope', 'cloudlet', new_cn)
            if new_bp:
                # Only delete the blueprint if cloudlet is being explicitly set
                # (i.e. user isn't just viewing current scope printout)
                self.app.config.set('scope', 'blueprint', new_bp)
            else:
                self.app.config.set('scope', 'blueprint', '')

            if new_cn != old_cn or new_bp != old_bp:
                print "Set default command scope to " + colored(new_cn, "cyan") + " " + colored(new_bp or "", "yellow")
                save_config(self)
        elif old_cn is '':
            print "Default command scope is unset. Run nepho scope <cloudlet> [blueprint] to set."
        else:
            print_scope(self)

    @controller.expose(help="unset current scope", aliases=['clear'])
    def unset(self):
        self.app.log.debug('Unsetting scope.')
        self.app.config.set('scope', 'cloudlet', '')
        self.app.config.set('scope', 'blueprint', '')
        save_config(self)

        print "Default command scope is now unset. Run nepho scope <cloudlet> [blueprint] to set."


def print_scope(app_obj):
    if app_obj.app.config.get('scope', 'cloudlet') is not '':
        print base.DISP_DASH * 80
        print " Using default command scope " + colored(app_obj.app.config.get('scope', 'cloudlet'), "cyan") + " " + colored(app_obj.app.config.get('scope', 'blueprint') or "", "yellow")
        print base.DISP_DASH * 80
    else:
        pass


def save_config(app_obj):
    # Write out the working configuration to the lowest accessible config file
    # on the stack after stripping extraneuous values. This has gotten quite
    # convoluted and now I am regretting the whole exercise of using built-in
    # config handling vs rolling our own.
    config_files = app_obj.app._meta.config_files
    config_files.reverse()
    config_obj = copy(app_obj.app.config)
    for section in [section for section in config_obj.sections() if section.find('controller.') != -1]:
        config_obj.remove_section(section)
    config_obj.remove_section('log')
    for cf in config_files:
        if os.access(os.path.dirname(cf), os.W_OK | os.X_OK):
            try:
                with open(cf, 'wb') as configfile:
                    config_obj.write(configfile)
                break
            except:
                pass
        else:
            continue
    else:
        print "Unable to write Nepho configuration -- no writable config file location found."
        print "Possible locations are: %s" % (app_obj.app._meta.config_files)
