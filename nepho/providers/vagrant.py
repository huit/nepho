# coding: utf-8

from os import path  
import yaml

import nepho
#from nepho.core import common, resource
#from nepho.core import  provider
#import nepho.core.provider 
             
class VagrantProvider(nepho.core.provider.AbstractProvider):   
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "vagrant"
    TEMPLATE_FILENAME = "Vagrantfile"
    
    def deploy(self):
        """Deploy a given pattern."""
        print self.pattern.template
        self.resourceManager.load_template(self.pattern.template)
        
        
        
    
    def undeploy(self):
        pass
        
  