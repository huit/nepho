#!/usr/bin/env python
from cement.core import controller
from nepho.cli import base
from nepho.core import cloudlet

class NephoCloudletController(base.NephoBaseController):
    class Meta:
        label = 'cloudlet'
        stacked_on = None
        description = 'find, download, and manage cloudlets'
        usage = "nepho cloudlet <action> [options]"

    @controller.expose()
    def list(self):
    	cloudlet.list(self)