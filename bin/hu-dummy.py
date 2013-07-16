#!/usr/bin/env python

# Dummy driver for a simple CLI, which uses aws-cli
#
#   https://github.com/aws/aws-cli
#
# This simple code is mostly taken from awscli.clidriver
#
# 

import sys
import logging

import botocore.session
from botocore.hooks import first_non_none_response
from botocore.hooks import HierarchicalEmitter
from botocore import xform_name
from botocore.compat import copy_kwargs, OrderedDict

from awscli import clidriver

import awscli.clidriver
from awscli import EnvironmentVariables, __version__
from awscli.formatter import get_formatter
from awscli.paramfile import get_paramfile
from awscli.plugin import load_plugins
from awscli.argparser import MainArgParser
from awscli.argparser import ServiceArgParser
from awscli.argparser import OperationArgParser
#from awscli.help import ProviderHelpCommand
#from awscli.help import ServiceHelpCommand
#from awscli.help import OperationHelpCommand
from awscli.argprocess import unpack_cli_arg


LOG = logging.getLogger('hu-dummy')

def setup_awscli_driver():
    emitter = HierarchicalEmitter()
    session = botocore.session.Session(EnvironmentVariables, emitter)
    session.user_agent_name = 'aws-cli'
    session.user_agent_version = __version__
    load_plugins(session.full_config.get('plugins', {}), event_hooks=emitter)
    return awscli.clidriver.CLIDriver(session=session)
            
def main():
    # Create an aws-cli driver
    driver = setup_awscli_driver()
    
    main_args=['ec2', 'describe-instances']
    return driver.main(main_args)

if __name__ == '__main__':
    sys.exit(main())
    
