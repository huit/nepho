# coding: utf-8
from os import path

import yaml
from nepho.core import common, resource, pattern


import botocore.session
import botocore.hooks
#import botocore.xform_name
from botocore.hooks import first_non_none_response
from botocore.hooks import HierarchicalEmitter

from botocore.compat import copy_kwargs, OrderedDict

import awscli
import awscli.clidriver
import awscli.plugin
#import awscli.argparser
#from awscli import clidriver

#import awscli.clidriver
#from awscli import EnvironmentVariables, __version__
# from awscli.formatter import get_formatter
# from awscli.paramfile import get_paramfile
# from awscli.plugin import load_plugins
# from awscli.argparser import MainArgParser
# from awscli.argparser import ServiceArgParser
# from awscli.argparser import OperationArgParser
# from awscli import clidriver

#import awscli.clidriver

        
class AWSProvider:
    """An infrastructure provider class for Vagrant"""

    PROVIDER_ID = "aws"
    TEMPLATE_FILENAME = "cf.json"
    
    def __init__(self):
        
        self.clidriver = self.setup_aws_driver()
        
    def setup_awscli_driver():
        envvars = awscli.EnvironmentVariables
        emitter = botocore.hooks.HierarchicalEmitter()
        session = botocore.session.Session(envvars, emitter)

        session.user_agent_name = 'aws-cli'
        session.user_agent_version = awscli.__version__
        load_plugins(session.full_config.get('plugins', {}), event_hooks=emitter)
        return awscli.clidriver.CLIDriver(session=session)
            
    def deploy(self):
        """Deploy a given pattern."""
        print self.pattern.template
    
    def undeploy(self):
        pass
        
#
# Methods pulled from old code, to be integrated.        
#
    
    def get_cf_template(pattern, context):
    
        cf_dir = resource_filename('nepho.aws', 'data/patterns/%s') % (pattern)
        cf_filename='template.cf'
        cf_file = '%s/%s' % (cf_dir, cf_filename)
        #paramsMap['template_file'] = cf_file
    
        # Use Jinja2
        template_dirs = [cf_dir, resource_filename('nepho.aws', 'data/patterns/common')]
        jinjaFSloader = FileSystemLoader(template_dirs)
        env = Environment(loader=jinjaFSloader)
        jinja_template = env.get_template(cf_filename)
    
        # Render it
        return jinja_template.render(context)


    def parse_cf_json(str):
        cf_dict =  json.loads(str, object_pairs_hook=collections.OrderedDict)
        return cf_dict
    
    def get_cf_json(orderDict, pretty=False):
        outstr = None
        if pretty:
            outstr = json.dumps(orderDict, indent=2, separators=(',', ': '))
        else:
            outstr = json.dumps(orderDict)
        return outstr