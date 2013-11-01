# coding: utf-8
from os import path
import yaml

from nepho.providers import *


class ProviderFactory:
    """A factory that creates provider-specific driver classes"""
    
    def create(self, name, config):
        
        # TODO: do something clever here by parsing the "providers" module and contents.
        
        if name == "vagrant":
            return vagrant.VagrantProvider(config)
        
        if name == "aws":
            return aws.AWSProvider(config)
        
        if name == "ansible":
            return ansible.AnsibleProvider(config)
    