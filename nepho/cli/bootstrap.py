import sys
from cement.core import hook, handler
from cement.utils import fs
from nepho import cli

# Capture and translate ANSI terminal escape sequences for Windows
from colorama import init
init()


def load():
    # Subcontrollers for each functional component
    handler.register(cli.cloudlet.NephoCloudletController)
    handler.register(cli.blueprint.NephoBlueprintController)
    handler.register(cli.stack.NephoStackController)
    handler.register(cli.parameter.NephoParameterController)
    handler.register(cli.scope.NephoScopeController)

    hook.register('post_argument_parsing', cli.hooks.set_scope)
    hook.register('post_setup', cli.hooks.process_config)


def run():
    # Load the base Nepho cement controller
    app = cli.base.Nepho()

    try:
        app.setup()
        app.run()
    finally:
        app.close()
