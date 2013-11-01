# coding: utf-8
import yaml
#from nepho.core import common
from os import path

#from nepho.core import common, cloudlet, provider

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
    