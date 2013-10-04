#!/usr/bin/env python
from nepho.cli import base

class NephoStackController(base.NephoBaseController):
    class Meta:
        label = 'stack'
        stacked_on = None
        description = 'create, manage, and destroy stacks built from scenarios'
        usage = "nepho stack <action> [options]"