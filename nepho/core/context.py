# coding: utf-8
import yaml
#from nepho.core import common
from os import path

class ContextManager:
    """
        A configuration handler class for Nepho. 
        
        Currently wraps ConfigParser object, but could be reimplemented
        as needed. Basically defines getters an setters.
        
        Saves the state on every set invocation.
        
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
        context['config'] = self.configManager.to_dict()
        
        if self.blueprint is not None:
            cloudlt = self.blueprint.cloudlet
            context['cloudlet'] = cloudlt.defn
            context['blueprint '] = self.blueprint.defn
                            
#         context = pattern.get_context()
#         context['config'] = self.config.to_dict()
#         try:
#             context[providr.PROVIDER_ID] = self.config.to_dict(providr.PROVIDER_ID)
#         except:
#             pass 
#         
#         try:
#             context['parameters'] = self.config.to_dict("parameters")
#         except:
#             pass 
#         #context['cloudlet'] 
        
        return context
    
        
# 
# 
#         
#         
#     
#             
#     def keys(self, domain="nepho"):
#         """Return a set of config names"""
#         return self.ini_config.keys(domain)
#         
#        
#     def load(self, config_file):
#         """Load in configs from local settings YAML file."""
#         try:
#             cnfg = yaml.load(open(config_file))
#             for k in cnfg.keys():
#                 self.set(k, cnfg[k])
#         except Exception as e:
#             pass
#     
#     def save(self):
#         """Saves out configs to the local config file."""
#         d = self.to_dict()
#         config_file = self.get("local_config")
#         
#         try:
#             cnfg = yaml.dump(d, open(config_file, "w"))
#         except Exception as e:
#                 print "Error writing nepho local config YAML file!"
#                 print e
#                 exit(1)      
#                 
#                 
#     def get(self, key, domain="nepho"):
#         """Basic getter for config values."""
#         if domain is None:
#             domain = "nepho"
#         return self.ini_config.get(domain, key)
#                         
#                         
#     def set(self, key, value, domain="nepho"):  
#         """Basic setter for config values."""
#         if domain is None:
#             domain = "nepho"
#         self.ini_config.set(domain, key, value)
#         self.save()
#             
#             
#     def to_dict(self, domain="nepho"):
#         """Converts the configs to a dictionary for convenience"""
#         d = dict()
#         for k in self.keys():
#             d[k] = self.get(k)
#         return d

