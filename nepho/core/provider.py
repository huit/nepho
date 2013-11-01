# coding: utf-8
from os import path
import yaml

from nepho.core import common, resource, pattern

class AbstractProvider:
    """An abstract infrastructure provider class."""
    
    def __init__(self, config):

        self.pattern_name = None
        self.provider_id = None
        self.template_filename = None
        self.config = config
        self.resourceManager = resource.ResourceManager(self.config)

    def load_pattern(self, blueprint):
        pattern_str = blueprint.pattern()
        self.pattern_file = self.resourceManager.lookup_pattern_file(blueprint, self)
        self.pattern = pattern.Pattern(pattern_str,self.pattern_file)
        self.pattern.set_provider(self)
                
    def get_pattern(self):
        return self.pattern
        
    def deploy(self):
        pass
    
    def status(self):
        pass
    
    def access(self):
        pass
    
    def destroy(self):
        pass
           
          