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
#        self.provider = None
        self.transient_params = dict()
            

    def set_blueprint(self, bprint):
        self.blueprint = bprint
        
#    def set_provider(self,providr):
#        self.provider = providr
        
    def add_params(self, params):
        self.transient_params = params
        
    def generate(self):
        """Generates a context object to be injected into the templating engine."""
        
        context = dict()
        config = self.configManager.to_dict()
            
        # construct the parameters data structure    
        context['parameters'] = dict()            
        if "parameters" in config:
            context['parameters'] = copy.copy(config['parameters'])
        if self.transient_params is not None:
            for (k,v) in self.transient_params.items():
                 context['parameters'][k] = v         
                    
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
  