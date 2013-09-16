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

from pkg_resources import resource_filename

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
import argparse

from jinja2 import Environment, FileSystemLoader

import json
import collections
import yaml
import string
import random

from nepho.command import command
#from nepho.aws import Deployment
#from nepho.aws import Template

__MODULE_NAME__     = "nepho"
__DEPLOYMENTS_DIR__ = 'data/deployments'
__PATTERNS_DIR__    = 'data/patterns'
__DRIVERS_DIR__     = 'data/drivers'

__PASSWORD_REPLACE_FLAG__ = 'NEPHO_CHANGEME_PASSWORD'

LOG = logging.getLogger(__MODULE_NAME__)

def gimme_random_password(lngth=32):

    alpha_char_set =  string.ascii_uppercase + string.ascii_lowercase
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    first = random.sample(alpha_char_set,1)
    rest = ''.join(random.sample(char_set*(lngth-1),lngth-1))
    return "%s%s" % (first[0], rest)

def setup_awscli_driver():
    emitter = HierarchicalEmitter()
    session = botocore.session.Session(EnvironmentVariables, emitter)
    session.user_agent_name = 'aws-cli'
    session.user_agent_version = __version__
    load_plugins(session.full_config.get('plugins', {}), event_hooks=emitter)
    return awscli.clidriver.CLIDriver(session=session)

def scan_deployments(deployment_dir=resource_filename(__MODULE_NAME__, __DEPLOYMENTS_DIR__)):
    from os import listdir
    from os.path import isfile, join
    files = [ f for f in listdir(deployment_dir) if isfile(join(deployment_dir,f)) ]

    deployDict = dict()
    for filename in files:
        deployment_name = string.replace(filename, ".yaml", "")
        f = open("%s/%s" % (deployment_dir, filename))
        fDict = yaml.safe_load(f)
        f.close()
        deployDict[deployment_name] = fDict

    return deployDict

def load_deployment_file(deployment, environment):
    """
        Takes in a YAML deployment file and environment setting and
            returns a dict of values
    """
    paramsMap = dict()
    yaml_file = resource_filename(__MODULE_NAME__, '%s/%s.yaml') % (__DEPLOYMENTS_DIR__, deployment)
    try:
        f = open(yaml_file)
        yamlMap = yaml.safe_load(f)
        f.close()

        if not yamlMap.has_key(environment):
            print "Environment \"%s\" is not present in deployment file %s" % (environment, yaml_file)
            sys.exit(1)

        envMap = yamlMap[environment]
        for k in envMap.keys():
            paramsMap[k] = envMap[k]
    except IOError as e:
        print "Error parsing deployment file \"%s\"" % (yaml_file)
        print " Check for the file and that it is properly formatted YAML."
        print "Error:"
        print e
        sys.exit(1)

    return paramsMap

def load_user_data_script(script_filename):
    "loads a scripts and returns it in a JSON-encoded format suitable for injection"
    script_array = []
    f = open(script_filename)
    for line in f:
        lstr = json.dumps(line.strip() + "\n")
        script_array.append(lstr)
    f.close()
    return script_array

def get_management_settings(map):
    " Returns dict as a context for the template for how to handle system management"
    management = None

    if map.has_key('management'):
        management = map.pop('management')

    user_data_scripts = dict()
    mgmt_script_dir   = resource_filename(__MODULE_NAME__, __DRIVERS_DIR__)
    drivers_dir = resource_filename(__MODULE_NAME__, __DRIVERS_DIR__)
    mgmt_script_file  = None

    pkgs = []

    if management == 'none':
        pkgs = [ "httpd" ]

    if management == 'script':
        mgmt_script_dir   = resource_filename(__MODULE_NAME__, __DEPLOYMENTS_DIR__)
        mgmt_script_file = '%s/%s' % (mgmt_script_dir, map.pop('script'))
        pkgs= ['bash']

    if management == 'puppet':
        mgmt_script_file = '%s/%s' % (mgmt_script_dir, 'puppet-snippet.sh')
        pkgs = ["gcc", "ruby","ruby-devel", "rubygems", "puppet" ]

    if map.has_key('packages'):
        for pkg in map['packages']:
            pkgs.append(pkg)
        map.pop('packages')

    # Load script into a array of lines
    if mgmt_script_file is not None:
        user_data_scripts['management'] = load_user_data_script(mgmt_script_file)
    else:
        user_data_scripts['management'] = []

    # Load other helper scripts
    cf_pre_script  = '%s/%s' % (drivers_dir, 'cf-pre-script.sh')
    user_data_scripts['cf_pre_script'] = load_user_data_script(cf_pre_script)

    cf_init_script = '%s/%s' % (drivers_dir, 'cf-init-script.sh')
    user_data_scripts['cf_init_script'] = load_user_data_script(cf_init_script)
        
    cf_post_script = '%s/%s' % (drivers_dir, 'cf-post-script.sh')
    user_data_scripts['cf_post_script'] = load_user_data_script(cf_post_script)
        
    
    mgmtMap = dict(
                     management = management,
                     scripts = user_data_scripts,
                     packages = pkgs
                   )

    return mgmtMap

def get_cf_template(pattern, context):

    cf_dir = resource_filename(__MODULE_NAME__, '%s/%s' % (__PATTERNS_DIR__, pattern) )
    cf_filename='template.cf'
    cf_file = '%s/%s' % (cf_dir, cf_filename)

    #paramsMap['template_file'] = cf_file

    # Use Jinja2
    template_dirs = [cf_dir, resource_filename(__MODULE_NAME__, '%s/common' % (__PATTERNS_DIR__))]
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
        
    password = gimme_random_password()   
    return string.replace(outstr, __PASSWORD_REPLACE_FLAG__, password)

def main(args_json=None):
    # Create an aws-cli driver
    aws_driver = setup_awscli_driver()

    # Read in command line options as JSON
    if args_json is None:
        args_json = command()
    args=json.loads(args_json)

    # Very basic parsing to determine deployment and environment to use
    plugin_name = args['subcmd']
    deployment_name = args['deployment']
    env_name = args['opts']['environment']

    if args['subcmd'] == 'list-deployments':
        deployments = scan_deployments()
        print "\nAvailable deployments and environments:"
        print "-----------------------------------------"
        for dk in deployments.keys():
            deployDict = deployments[dk]
            env_str = string.join( deployDict.keys(), ", " )
            print "  %s:  %s" % (dk, env_str)
        print ""

        sys.exit(0)

    # determine name of this deployment instance
    stack_name = '%s-%s' % (deployment_name, env_name)
    if args['opts']['name'] is not None and len(args['opts']['name']) > 1:
        stack_name = args['opts']['name']


    # Load settings from YAML deployment file
    paramsMap = load_deployment_file(deployment_name, env_name)


    pattern =  paramsMap['pattern']
    paramsMap.pop('pattern')

    # Determine how to manage deployed instances
    context = get_management_settings(paramsMap)  

    if args['subcmd'] == 'show-template':
        raw_template = get_cf_template(pattern, context)
        try:
            cf_dict = parse_cf_json(raw_template)
            
            print get_cf_json(cf_dict, pretty=True)
        except ValueError:
            print raw_template
        sys.exit(0)

    if args['subcmd'] == 'validate-template':
        raw_template = get_cf_template(pattern, context)
        print "Jinja2 template loading succeeded."
        try:
             cf_dict = parse_cf_json(raw_template)
        except ValueError as e:
            print "Invalid JSON: "
            print e
            print ""
            print "Raw text:"
            print "------------------------"
            print raw_template
            sys.exit(1)
        print "JSON valid."
        main_args=[
               'cloudformation',
               'validate-template',
               '--template-body', get_cf_json(cf_dict)
               ]
        return aws_driver.main(main_args)

        #print json.dumps(cf_json, sort_keys=True,indent=4, separators=(',', ': '))
    if args['subcmd'] == 'show-params':
        try:
             cf_dict = parse_cf_json( get_cf_template(pattern, context) )
        except ValueError as e:
            print "Invalid JSON: run the \"validate-template\" subcommand to debug."
            sys.exit(1)

        paramsJSON= cf_dict['Parameters']
        print "Template parameters:"
        print "---------------------------"
        print get_cf_json(paramsJSON, pretty=True)
        sys.exit(1)

    #
    # Load as JSON to validate it
    #
    try:
        cf_dict = parse_cf_json( get_cf_template(pattern, context) )
    except ValueError:
        print "Error parsing JSON"
        print get_cf_template(pattern,context)
        sys.exit(1)

    if args['subcmd'] == 'deploy':

        main_args=[
               'cloudformation',
               'create-stack',
               '--capabilities', 'CAPABILITY_IAM',
               '--disable-rollback',
               '--stack-name', stack_name
               ]
        if paramsMap is not None and len(paramsMap.keys()) > 0:
            main_args.append("--parameters")
            for key in paramsMap.keys():
                main_args.append("ParameterKey=%s,ParameterValue=%s" % (key, paramsMap[key]))
        
        main_args.append("--template-body")
        raw_templ = get_cf_template(pattern, context)
        templ_json = get_cf_json( parse_cf_json(raw_templ) )
        main_args.append( templ_json )
        
        return aws_driver.main(main_args)

    if args['subcmd'] == 'delete':

        main_args=[
               'cloudformation',
               'delete-stack',
               '--stack-name', stack_name
               ]
        return aws_driver.main(main_args)

    # If we end up here, then the subcommand is not known.
    print "Unknown subcommand \"%s\"." % (args['subcmd'])
    print "Run nepho --help for details."
    sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())

