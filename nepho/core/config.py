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

        self.ini_config = ini_config
        local_config = self.ini_config.get('nepho', 'local_config')
        self.load(local_config)      

        
    def keys(self):
        """Return a set of config names"""
        return self.ini_config.keys("nepho")
        
       
    def load(self, config_file):
        """Load in configs from local settings YAML file."""
        try:
            cnfg = yaml.load(open(config_file))
            for k in cnfg.keys():
                self.set(k, cnfg[k])
        except Exception as e:
            pass
    
    def save(self):
        """Saves out configs to the loca lconfig file."""
        d = self.to_dict()
        config_file = self.get("local_config")
        
        try:
            cnfg = yaml.dump(d, open(config_file, "w"))
        except Exception as e:
                print "Error writing nepho local config YAML file!"
                print e
                exit(1)  
        
                
    def get(self, key, domain="nepho"):
        """Basic getter for config values."""
        if domain is None:
            domain = "nepho"
        return self.ini_config.get(domain, key)
                        
    def set(self, key, value, domain="nepho"):  
        """Basic setter for config values."""
        if domain is None:
            domain = "nepho"
        self.ini_config.set(domain, key, value)
        self.save()
            
    def to_dict(self):
        """Converts the configs to a doctionary for convenience"""
        d = dict()
        for k in self.keys():
            d[k] = self.get(k)
        return d

