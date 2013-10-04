#!/usr/bin/env python
from cement.core import backend, foundation, controller

class NephoStackController(controller.CementBaseController):
    class Meta:
        label = 'stack'
        stacked_on = None
        description = 'create, manage, and destroy stacks built from cloudlet scenarios'
