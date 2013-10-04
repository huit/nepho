#!/usr/bin/env python
from cement.core import backend, foundation, controller, handler

class NephoBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Command line cross-cloud orchestration tool for constructing virtual datacenters."
        usage = "nepho <sub-command> [options] <action> [options]"

    @controller.expose(hide=True)
    def default(self):
        print("Run nepho --help for a list of sub-commands.")

class Nepho(foundation.CementApp):
    class Meta:
        label = 'nepho'
        base_controller = NephoBaseController
