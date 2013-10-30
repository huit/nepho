# coding: utf-8
import yaml
from nepho.core import common
from os import path
from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint

class Blueprint:
    """A simple example class"""
    
    def __init__(self):
        self.defn = None


class BlueprintManager:
    """A simple example class"""
    
    def __init__(self):
        self.defn = None
            
    def all_blueprints(self, name):
        cloudlet = find_cloudlet(self, name)
        blueprint_files = list()
        if path.isdir(path.join(cloudlet, "blueprints")):
            blueprint_files.extend(glob.glob(path.join(cloudlet, "blueprints", '*.yaml')))
            return blueprint_files
        else:
            return None
    
    def find_blueprint(self, cloudlet, name):
        blueprint_paths = all_blueprints(self, cloudlet)
        paths = [path for path in blueprint_paths if name in path]
        return paths[0]

    
    
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

def load_blueprint(self, cloudlet, name):

    cy = None
    try:
        blueprint_common_file = common.find_blueprint(self, cloudlet, "common")
        cy = yaml.load(open(blueprint_common_file))
        
    except:
        pass

                    
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
    
    # copy over any common fields that were not overridden
    if cy is not None:
        for k in cy.keys():
            if not y.haskey(k):
                y[k] = cy[k]
    
    return y
            
def describe_blueprint(self, cloudlet, name):

    y = load_blueprint(self,cloudlet, name)

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
