# coding: utf-8
from os import path
import yaml

from nepho.core import common, resource, context, pattern

class AbstractProvider:
    """An abstract infrastructure provider class."""
    
    def __init__(self, config):

        self.config = config
        self.resourceManager = resource.ResourceManager(self.config)
        self.contextManager = context.ContextManager(self.config)
        
        self.blueprint = None
        self.pattern = None
        #self.provider_id = None
        #self.template_filename = None
        
    def load_pattern(self, blueprint):
        """Loads in a blueprint, looks up the pattern, and configures the context."""
        self.blueprint = blueprint
        pattern_str = blueprint.pattern()
        pattern_file = self.resourceManager.lookup_pattern_file(blueprint, self)
        self.pattern = pattern.Pattern(pattern_str, pattern_file)
        self.pattern.set_provider(self)
        self.contextManager.set_blueprint(self.blueprint)
        
        return self.pattern
                
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
           
          