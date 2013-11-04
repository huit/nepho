#!/usr/bin/env python

from os import path, makedirs
import re

from cement.core import backend, foundation, controller

import nepho.core.config

defaults = backend.defaults('nepho', 'base')
defaults['nepho']['archive_dir']           = path.join("~", ".nepho", "archive")
defaults['nepho']['tmp_dir']               = path.join("~", ".nepho", "tmp")
defaults['nepho']['cache_dir']             = path.join("~", ".nepho", "cache")
defaults['nepho']['cloudlet_dirs']         = path.join("~", ".nepho", "cloudlets")
defaults['nepho']['local_dir']             = path.join("~", ".nepho", "local")
defaults['nepho']['local_config']          = path.join("~", ".nepho", "local/config.yaml")
defaults['nepho']['cloudlet_registry_url'] = "http://cloudlets.github.io/registry.yaml"
defaults['base']['processed_config'] = False


class NephoBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Command line cross-cloud orchestration tool for constructing virtual datacenters."
        usage = "nepho <command> <action> [options]"

    def _setup(self, app):
        super(NephoBaseController, self)._setup(app)

        # Running this section twice (once for base and once for the subclassed
        # controller) causes errors. There is no doubt a better way to avoid
        # that behavior than this silly cheat...
        if self.config.get('base', 'processed_config') is not True:
            self.config.set('base', 'processed_config', True)

            # Multiple cloudlet dirs in a string need to be split into a list and
            # excess whitespace removed
            cloudlet_dirs = self.config.get('nepho', 'cloudlet_dirs').split(',')
            cloudlet_dirs = map(lambda x: x.strip(), cloudlet_dirs)
            self.config.set('nepho', 'cloudlet_dirs', cloudlet_dirs)

            # Do some pre-processing on all configuration items
            for key in self.config.keys('nepho'):
                value = self.config.get('nepho', key)

                if isinstance(value, list):
                    # Expand user where necessary
                    value = map(lambda x: path.expanduser(x), value)
                    self.config.set('nepho', key, value)

                    # If items are directories, make sure they exist
                    if re.search('_dirs$', key):
                        for one_dir in value:
                            if not path.exists(one_dir):
                                makedirs(one_dir)
                else:
                    # Expand user where necessary
                    value = path.expanduser(value)
                    self.config.set('nepho', key, value)

                    # If item is a directory, make sure it exists
                    if re.search('_dir$', key) and not path.exists(value):
                        makedirs(value)

        self.my_shared_obj = dict()
        
        self.nepho_config = nepho.core.config.ConfigManager(self.config)
        

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
