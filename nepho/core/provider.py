# coding: utf-8
from os import path
import yaml

from nepho.core import common, resource, context, pattern

class AbstractProvider:
    """An abstract infrastructure provider class."""
    
    def __init__(self, config, scenario=None):

        self.config = config
        self.scenario = scenario
        
        self.resourceManager = resource.ResourceManager(self.config)
        self.contextManager = context.ContextManager(self.config)
        
        
    def set_scenario(self, scenario):
        self.scenario = scenario

    def get_scenario(self):
        return self.scenario
                
    def validate_template(self, template):
        pass
    
    def format_template(self, template):
        return template
    
    def deploy(self):
        pass
    
    def status(self):
        pass
    
    def access(self):
        pass
    
    def destroy(self):
        pass
           
          