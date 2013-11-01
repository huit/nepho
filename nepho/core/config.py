# coding: utf-8
import yaml
#from nepho.core import common
from os import path

class ConfigManager:
    """
        A configuration handler class for Nepho. 
        
        Currently wraps ConfigParser object, but could be reimplemented
        as needed. Basically defines getters an setters.
    """
    
    def __init__(self, ini_config):

        self.ini_config = ini_config
        
    def get(self, key, domain=None):
        """Basic getter for config values."""
        if domain is None:
            domain = "nepho"
        return self.ini_config.get(domain, key)
                        
    def set(self, key, value, domain=None):  
        """Basic setter for config values."""
        if domain is None:
            domain = "nepho"
        self.config.set(domain, key, value)
            
        

