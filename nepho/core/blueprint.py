# coding: utf-8
import yaml
from nepho.core import common
from os import path
from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint


def list_blueprint(self, name):
    cloudlet = common.find_cloudlet(self, name)

    # Basically the same output as list_cloudlets
    dir = path.dirname(cloudlet)
    print colored(dir, "cyan")
    try:
        y = yaml.load(open(path.join(cloudlet, 'cloudlet.yaml')))
    except IOError:
        print colored("└──", "yellow"), name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
        exit(1)
    else:
        print colored("└──", "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"

    # Prepare to wrap description text
    wrapper = TextWrapper(width=80, initial_indent="        ", subsequent_indent="        ")

    # Now list the available blueprints
    for blueprint_file in common.all_blueprints(self, name):
        blueprint_name = path.basename(blueprint_file).rstrip(".yaml")
        try:
            y = yaml.load(open(blueprint_file))
        except:
            print colored("    └──", "yellow"), colored(blueprint_name, attrs=['underline'])
            print colored("        Error - missing or malformed cloudlet.yaml", "red")
        else:
            print colored("    └──", "yellow"), colored(blueprint_name, attrs=['underline'])
            print wrapper.fill(y['summary'])

    return


def describe_blueprint(self, cloudlet, name):
    try:
        blueprint_file = common.find_blueprint(self, cloudlet, name)
    except:
        print "Invalid cloudlet or blueprint name provided."
        exit(1)

    try:
        y = yaml.load(open(blueprint_file))
    except:
        print "Error loading blueprint YAML file!"
        exit(1)

    wrapper = TextWrapper(width=80, subsequent_indent="              ")

    print "-" * 80
    print "Name:         %s" % (y['name'])
    print "Provider:     %s" % (y['provider'])
    print wrapper.fill("Summary:      %s" % (y['summary']))
    print wrapper.fill("Description:  %s" % (y['description']))
    print "-" * 80

    p = y.pop('parameters', None)

    pprint(p)

    print "-" * 80
    return
