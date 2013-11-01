# coding: utf-8
import yaml
from nepho.core import common
from os import path

class Pattern:
    """An infrastructure design pattern class"""
    
    def __init__(self, blueprint, pattern_name):

        self.name = pattern_name
        self.blueprint = blueprint
        
        self.pattern_dir = loopkup_pattern(pattern_name)
        
        # now load definition, and fail is unable
        self.defn = None
        if self.file is not None:
            try:
                self.defn = yaml.load(open(blueprint_file))
            except Exception as e:
                print "Error loading blueprint YAML file at %s!" % (blueprint_file)
                exit(1)
        self.name =  path.basename(blueprint_file).rstrip(".yaml")
        self.defn['name'] = self.name

    
            
        

