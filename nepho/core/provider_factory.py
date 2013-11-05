# coding: utf-8
from os import path
import yaml

from nepho.providers import vagrant_provider, aws_provider


class ProviderFactory:
    """A factory that creates provider-specific driver classes"""
    
    def create(self, name, config, scenario=None):
        
        # TODO: do something clever here by parsing the "providers" module and contents.
        
        if name == "vagrant":
            return vagrant_provider.VagrantProvider(config, scenario)
        
        if name == "aws":
            return aws_provider.AWSProvider(config, scenario)
        
#        if name == "ansible":
#            return ansible.AnsibleProvider(config)
    