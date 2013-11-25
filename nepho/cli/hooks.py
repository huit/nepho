import os
from termcolor import colored
import re


def process_config(app_obj):
    # Multiple cloudlet dirs in a string need to be split into a list and
    # excess whitespace removed
    cloudlet_dirs = app_obj.config.get('nepho', 'cloudlet_dirs').split(',')
    app_obj.cloudlet_dirs = map(lambda x: os.path.expanduser(x.strip()), cloudlet_dirs)
    for dir in [dir for dir in app_obj.cloudlet_dirs if not os.path.exists(dir)]:
        os.makedirs(dir)

    # For all file and directory items, make sure path is expanded
    for key in [key for key in app_obj.config.keys('nepho') if re.search('_(dirs?|file)$', key)]:
        value = app_obj.config.get('nepho', key)
        # Expand user where necessary
        value = os.path.expanduser(value)
        app_obj.config.set('nepho', key, value)

        # If item is a directory, make sure it exists
        if re.search('_dir$', key) and not os.path.exists(value):
            os.makedirs(value)


def set_scope(app_obj):
    """
    Choose and set correct cloudlet and blueprint names to operate on.
    Precedence is configured scope, command line argument, None. If cloudlet is
    configured and only the cloudlet argument is passed, assign it to blueprint.
    """
    if app_obj.config.get('scope', 'cloudlet') is not '':
        app_obj.cloudlet_name = app_obj.config.get('scope', 'cloudlet')
    else:
        try:
            app_obj.cloudlet_name = app_obj.pargs.cloudlet
        except:
            # Nepho is called with no subcommand
            app_obj.cloudlet_name = None

    if app_obj.config.get('scope', 'blueprint') is not '':
        app_obj.blueprint_name = app_obj.config.get('scope', 'blueprint')
    elif hasattr(app_obj.pargs, 'blueprint') and app_obj.pargs.blueprint is not None:
        app_obj.blueprint_name = app_obj.pargs.blueprint
    elif app_obj.config.get('scope', 'cloudlet') is not '':
        app_obj.blueprint_name = app_obj.pargs.cloudlet
    else:
        app_obj.blueprint_name = None
