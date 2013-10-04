#!/usr/bin/env python
from cement.core import backend, foundation, controller, handler

# define a second controller
class NephoCloudletController(controller.CementBaseController):
    class Meta:
        label = 'cloudlet'
        stacked_on = None
        description = 'find, download, and manage cloudlets'
