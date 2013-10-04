#!/usr/bin/env python
from nepho.cli import base

class NephoScenarioController(base.NephoBaseController):
    class Meta:
        label = 'scenario'
        stacked_on = None
        description = 'list and view individual cloudlet deployment scenarios'
        usage = "nepho scenario <action> [options]"