# coding: utf-8
import yaml
from nepho.core import common, resource, pattern
from os import path


class ProviderFactory:
    """A factory that creates provider-specific driver classes"""
    
    def create(self, name, config):
        
        if name == "vagrant":
            return VagrantProvider(config)
        
        if name == "aws":
            return AWSProvider(config)
        
        if name == "ansible":
            return None
    

        
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
                
    def get_pattern(self, pattern):
        self.pattern_name = pattern           
             
class VagrantProvider(AbstractProvider):   
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "vagrant"
    TEMPLATE_FILENAME = "Vagrantfile"
    
    def deploy(self):
        """Deploy a given pattern."""
        print self.pattern.template
        
    
    def undeploy(self):
        pass
        
        
class AWSProvider:
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "aws"
    TEMPLATE_FILENAME = "cf.json"
    
    def deploy(self):
        """Deploy a given pattern."""
        print self.pattern.template
    
    def undeploy(self):
        pass
        

class AnisbleProvider:
    """An infrastructure provider class for ansible"""

    PROVIDER_ID = "ansible"
    TEMPLATE_FILENAME = "playbook.yaml"
    
    def deploy(self):
        """Deploy a given pattern."""
        pass
    
    def undeploy(self):
        pass
                
                
        
            
            
