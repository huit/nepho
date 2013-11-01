# coding: utf-8
import yaml
#from nepho.core import common
from os import path

import jinja2

#from jinja2 import Environment, FileSystemLoader
from nepho.core import common, cloudlet

class ResourceManager:
    """
        A resource handler class for Nepho. 
        
        Used to do loopkups on patterns, blueprints, etc.

    """
    
    def __init__(self, config):

        self.config = config  

    def lookup_pattern_dir(self, blueprint):
        """Given a blueprint and pattern name/string, lookup and return that pattern directory."""  
        
        pattern_string = blueprint.pattern().name
        main_cloudlet = blueprint.cloudlet
        cloudlt = main_cloudlet
        pattern_name = pattern_string           
        if ">" in pattern_string:
            (cloudlet_name, pattern_name) = pattern_string.split(">")
            cloudlt = cloudlet.CloudletManager(self.config).find(cloudlet_name)

        pattern_dir = path.join(cloudlt.path, "resources", "patterns", pattern_name)
        return pattern_dir        


    def lookup_pattern_file(self, blueprint, provider):
        """Given a blueprint and pattern name/string, lookup and return that pattern file."""  
        pattern_dir = self.lookup_pattern_dir(blueprint)        
        pattern_file = path.join(pattern_dir, provider.PROVIDER_ID, provider.TEMPLATE_FILENAME)
        return pattern_file
    
    def render_template(self, pattern):
        """ convert a template file into a rendered string."""
        template_file_abs = pattern.get_template_file()
        
        tdir = path.dirname(template_file_abs)
        template_file = path.basename(template_file_abs)
        template_dirs = [tdir]
        context = pattern.get_context()
    
        # Use Jinja2
        jinjaFSloader = jinja2.FileSystemLoader(template_dirs)
        env = jinja2.Environment(loader=jinjaFSloader)     
        jinja_template = env.get_template(template_file)
    
        # Render it
        templ = None
        try:
            templ = jinja_template.render(context)
        except TemplateNotFound:
            print colored("Error finding template file %s" % (template_file), "red")
            print colored("Template search path %s" % (template_file), "red")
            exit(1)
        
        return templ



        
        
    