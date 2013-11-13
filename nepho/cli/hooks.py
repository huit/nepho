from os import path, makedirs
from termcolor import colored
from nepho.core.config import ConfigManager
import re


def process_config(self):
    # Multiple cloudlet dirs in a string need to be split into a list and
    # excess whitespace removed
    cloudlet_dirs = self.config.get('nepho', 'cloudlet_dirs').split(',')
    cloudlet_dirs = map(lambda x: x.strip(), cloudlet_dirs)
    self.config.set('nepho', 'cloudlet_dirs', cloudlet_dirs)

    # Do some pre-processing on all configuration items
    for key in self.config.keys('nepho'):
        value = self.config.get('nepho', key)

        if isinstance(value, list):
            # Expand user where necessary
            value = map(lambda x: path.expanduser(x), value)
            self.config.set('nepho', key, value)

            # If items are directories, make sure they exist
            if re.search('_dirs$', key):
                for one_dir in value:
                    if not path.exists(one_dir):
                        makedirs(one_dir)
        else:
            # Expand user where necessary
            value = path.expanduser(value)
            self.config.set('nepho', key, value)

            # If item is a directory, make sure it exists
            if re.search('_dir$', key) and not path.exists(value):
                makedirs(value)

    self.nepho_config = ConfigManager(self.config)


def set_scope(app):
    """
    Choose and set correct cloudlet and blueprint names to operate on.
    Precedence is configured scope, command line argument, None. If cloudlet is
    configured and only the cloudlet argument is passed, assign it to blueprint.
    """
    if app.nepho_config.get('scope_cloudlet') is not None:
        app.cloudlet_name = app.nepho_config.get('scope_cloudlet')
    else:
        try:
            app.cloudlet_name = app.pargs.cloudlet
        except:
            # Nepho is called with no subcommand
            app.cloudlet_name = None

    if app.nepho_config.get('scope_blueprint') is not None:
        app.blueprint_name = app.nepho_config.get('scope_blueprint')
    elif hasattr(app.pargs, 'blueprint') and app.pargs.blueprint is not None:
        app.blueprint_name = app.pargs.blueprint
    elif app.nepho_config.get('scope_cloudlet') is not None:
        app.blueprint_name = app.pargs.cloudlet
    else:
        app.blueprint_name = None
