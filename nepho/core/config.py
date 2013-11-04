# coding: utf-8
import yaml
#from nepho.core import common
from os import path

class ConfigManager:
    """
        A configuration handler class for Nepho. 
        
        Currently wraps ConfigParser object, but could be reimplemented
        as needed. Basically defines getters an setters.
        
        Saves the state on every set invocation.
        
    """
    
    def __init__(self, ini_config):

        self.data = dict()
        
        self.ini_config = ini_config
        local_config = self.ini_config.get('nepho', 'local_config')
        self.load(local_config)
        for (k,v) in self.ini_config.items('nepho'):
            self.data[k] = v         
        self.save()     

        
    def keys(self, domain=None):
        """Return a set of config names"""
        if domain is not None:
            if domain in self.data and isinstance(self.data[domain], dict):
                return self.data[domain].keys()
            else: 
                return dict()
        else:
            return self.data.keys()
                
                
    def get(self, key, domain=None):
        """Basic getter for config values."""
        if domain is not None:
             return self.data[domain][key]
        return self.data[key]
                        
                        
    def set(self, key, value, domain=None):  
        """Basic setter for config values."""
        if domain is not None:
             if domain in self.data and isinstance(self.data[domain], dict):
                 self.data[domain][key] = value
             else:
                 self.data[domain] = { key: value }
        else:
            self.data[key] = value
        self.save()
            
    def unset(self, key, domain=None):  
        """Basic setter for config values."""
        if domain is not None:
             if domain in self.data:
                 del self.data[domain][key]
        else:
            del self.data[key]
        self.save()
                    
    def to_dict(self, domain=None):
        """Converts the configs to a dictionary for convenience"""
        if domain is not None:
            if domain in self.data and isinstance(self.data[domain], dict):
                return self.data[domain]
            else:
                return None
        else:
            return self.data

       
    def load(self, config_file):
        """Load in configs from local settings YAML file."""
        try:
            self.data = yaml.load(open(config_file))
        except Exception as e:
            pass
    
    def save(self):
        """Saves out configs to the local config file."""
#         d = self.to_dict("*")
        config_file = self.get("local_config")
        
        try:
            cnfg = yaml.dump(self.data, open(config_file, "w"))
        except Exception as e:
                print "Error writing nepho local config YAML file!"
                print e
                exit(1)      
                
