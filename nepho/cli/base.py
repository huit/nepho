#!/usr/bin/env python
from cement.core import backend, foundation, controller, handler
from os import path

defaults = backend.defaults('nepho', 'global')
defaults['global']['cloudlets_path'] = path.join(path.expanduser("~"), ".nepho", "cloudlets")
defaults['global']['overrides_path'] = path.join(path.expanduser("~"), ".nepho", "overrides")

class NephoBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Command line cross-cloud orchestration tool for constructing virtual datacenters."
        usage = "nepho <command> <action> [options]"
        config_defaults = defaults

    def _setup(self, app):
        super(NephoBaseController, self)._setup(app)
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