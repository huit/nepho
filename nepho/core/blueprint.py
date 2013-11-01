# coding: utf-8
import yaml
from nepho.core import common, pattern
from os import path

class Blueprint:
    """A simple example class"""
    
    def __init__(self, cloudlt, blueprint_file):

        self.file = blueprint_file 
        self.cloudlet = cloudlt
        
        # now load definition, and fail is unable
        self.defn = None
        if self.file is not None:
            try:
                self.defn = yaml.load(open(blueprint_file))
            except Exception as e:
                print "Error loading blueprint YAML file at %s!" % (blueprint_file)
                exit(1)     
        self.name =  path.basename(blueprint_file).replace(".yaml", "")
        self.defn['name'] = self.name

    def pattern(self):
        """Returns a pattern object that represents the pattern in the blueprint."""
        patternString = self.defn['pattern']
        pattern = pattern.Pattern(self, patternString)
        return pattern
    
    def provider_name(self):
        """returns a provider pbjects that corresponds to the one indicated in the blueprint."""
        providerString = self.defn['provider']
        
        return providerString
    
            
        

