#!/usr/bin/env python
from cement.core import backend, foundation, controller

# define a second controller
class NephoScenarioController(controller.CementBaseController):
    class Meta:
        label = 'scenario'
        stacked_on = None
        description = 'list and view individual cloudlet deployment scenarios'
