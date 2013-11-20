#!/usr/bin/env python

from os import path, makedirs
import re

from cement.core import backend, foundation, controller
from cement.utils.misc import init_defaults

import nepho.core.config

defaults = init_defaults('nepho', 'internal')
defaults['nepho']['archive_dir']           = path.join("~", ".nepho", "archive")
defaults['nepho']['tmp_dir']               = path.join("~", ".nepho", "tmp")
defaults['nepho']['cache_dir']             = path.join("~", ".nepho", "cache")
defaults['nepho']['cloudlet_dirs']         = path.join("~", ".nepho", "cloudlets")
defaults['nepho']['local_dir']             = path.join("~", ".nepho", "local")
defaults['nepho']['local_config']          = path.join("~", ".nepho", "local", "config.yaml")
defaults['nepho']['cloudlet_registry_url'] = "http://cloudlets.github.io/registry.yaml"
defaults['nepho']['cloudlet_clone_proto']  = "https"
defaults['internal']['processed_config']   = False


class NephoBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Command line cross-cloud orchestration tool for constructing virtual datacenters."
        usage = "nepho <command> <action> [options]"

    def _setup(self, app):
        super(NephoBaseController, self)._setup(app)

    @controller.expose(hide=True)
    def default(self):
        if self._meta.label == "base":
            print "Run %s --help for a list of commands" % (self.app.args.prog)

        else:
            print "Run %s %s --help for a list of actions" % (self.app.args.prog, self._meta.label)


class Nepho(foundation.CementApp):
    class Meta:
        label = 'nepho'
        base_controller = NephoBaseController
        config_defaults = defaults
        bootstrap = 'nepho.cli.bootstrap'
