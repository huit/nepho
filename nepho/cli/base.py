#!/usr/bin/env python
from cement.core import backend, foundation, controller
from os import path

defaults = backend.defaults('nepho')
defaults['nepho']['archive_dir'] = path.join(path.expanduser("~"), ".nepho", "archive")
defaults['nepho']['cache_dir'] = path.join(path.expanduser("~"), ".nepho", "cache")
defaults['nepho']['cloudlet_dirs'] = path.join(path.expanduser("~"), ".nepho", "cloudlets")
defaults['nepho']['local_dir'] = path.join(path.expanduser("~"), ".nepho", "local")

defaults['nepho']['cloudlet_registry_url'] = "https://cloudlets.github.io/registry.yaml"


class NephoBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Command line cross-cloud orchestration tool for constructing virtual datacenters."
        usage = "nepho <command> <action> [options]"
        config_defaults = defaults

    def _setup(self, app):
        super(NephoBaseController, self)._setup(app)

        # Expand user where necessary
        for item in self.config.keys('nepho'):
            self.config.set('nepho', item, path.expanduser(self.config.get('nepho', item)))

        self.my_shared_obj = dict()

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
