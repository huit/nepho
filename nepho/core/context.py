# coding: utf-8
import yaml
import copy
#from nepho.core import common
from os import path

class ContextManager:
    """
        A context handler class for Nepho. 
        
        Produces a context dictionary for use with templating engines.
    """
    
    def __init__(self, cfgMgr):

        self.configManager = cfgMgr
        self.blueprint = None
        self.provider = None
            

    def set_blueprint(self, bprint):
        self.blueprint = bprint
        
    def set_provider(self,providr):
        self.provider = providr
        
    def generate(self):
        """Generates a context object to be injected into the templating engine."""
        
        context = dict()
        config = self.configManager.to_dict()
        if "parameters" in config:
            context['parameters'] = copy.copy(config['parameters'])
                    
        context['config'] = config
        
        if self.blueprint is not None:
            cloudlt = self.blueprint.cloudlet
            context['cloudlet'] = cloudlt.defn
            context['blueprint'] = self.blueprint.defn

        #
        # Temporary measure
        #
        context['scripts'] = None

        return context
  