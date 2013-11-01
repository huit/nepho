# coding: utf-8
import yaml
from nepho.core import common
from os import path

class ProviderFactory:
    """A factory that creates provider-specific driver classes"""
    
    def create(self, name):
        
        if name == "vagrant":
            return VagrantProvider()
        if name == "aws":
            return AWSProvider()
        if name == "ansible":
            return None
        
class AbstractProvider:
    """An abstract infrastructure provider class."""
    
    def __init__(self):

        self.pattern_name = None
                    
class VagrantProvider:
    """An infrastructure provider class for Vagrant"""
    
    def __init__(self):

        self.pattern_name = None
        
    def setPattern(self, pattern):
        self.pattern_name = pattern

    def deploy(self):
        """Deploy a given pattern."""
        pass
    
    def undeploy(self):
        pass
        
        
class AWSProvider:
    """An infrastructure provider class for Vagrant"""
    
    def __init__(self):

        self.pattern_name = None
        

    def setPattern(self, pattern):
        self.pattern_name = pattern

    def deploy(self):
        """Deploy a given pattern."""
        pass
    
    def undeploy(self):
        pass
        
        
                
        
            
            
