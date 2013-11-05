# coding: utf-8

from os import path
import yaml

from termcolor import colored
from textwrap import TextWrapper
from pprint import pprint

import jinja2

#from jinja2 import Environment, FileSystemLoader
from nepho.core import common, cloudlet

class ResourceManager:
    """
        A resource handler class for Nepho. 
        
        Used to do lookups on files, dirs, and templates for
           patterns, blueprints, etc.

    """
    
    def __init__(self, config):

        self.config = config  

    def lookup_pattern_dir(self, blueprint):
        """Given a blueprint and pattern name/string, lookup and return that pattern directory.
        
        For locally referenced patterns, assume that it's in the directories
        
           ./resources/patterns/[blueprint name]/
           
        or in a common directory at
        
           ./resources/patterns/common/
           
        If given with a cloudlet referenence (i.e. cloudlet_name > pattern_name) it
        looks up with the referenced cloudlet dir
        
          [cloudlet_name]/resources/patterns/pattern_name   

        """  
        
        pattern_string = blueprint.pattern().name

        main_cloudlet = blueprint.cloudlet
        cloudlt = main_cloudlet
        pattern_name = pattern_string           
        if ">" in pattern_string:
            (cloudlet_name, pattern_name) = pattern_string.split(">")
            cloudlet_name = cloudlet_name.strip()
            pattern_name = pattern_name.strip()
            cloudlt = cloudlet.CloudletManager(self.config).find(cloudlet_name)

        pattern_dir = path.join(cloudlt.path, "resources", "patterns", pattern_name)
        if not path.isdir(pattern_dir):
            pattern_dir = path.join(cloudlt.path, "resources", "patterns", "common")
        
        return pattern_dir        


    def lookup_pattern_file(self, blueprint, provider):
        """Given a blueprint and pattern name/string, lookup and return that pattern file."""  
        pattern_dir = self.lookup_pattern_dir(blueprint)        
        pattern_file = path.join(pattern_dir, provider.PROVIDER_ID, provider.TEMPLATE_FILENAME)

        return pattern_file
    
    def render_template(self, pattern, context):
        """Convert a template file into a rendered string."""
        providr = pattern.provider
        
        template_file_abs = pattern.get_template_file()
        template_dir = path.dirname(template_file_abs)
        template_common_dir = path.join(
                template_dir, "..", "..", "common", providr.PROVIDER_ID )
        
        template_file = path.basename(template_file_abs)
        template_dirs = [template_dir, template_common_dir]
    
        # Use Jinja2
        jinjaFSloader = jinja2.FileSystemLoader(template_dirs)
        env = jinja2.Environment(loader=jinjaFSloader)     
        jinja_template = env.get_template(template_file)
    
        # Render it with the provided context ...
        templ = None
        try:
            templ = jinja_template.render(context)
        except jinja2.TemplateNotFound:
            print colored("Error finding template file %s" % (template_file), "red")
            print colored("Template search path %s" % (template_dirs), "red")
            exit(1)
        
        return templ
