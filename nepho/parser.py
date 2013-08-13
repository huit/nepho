import argparse

__SUBCOMAMND_HELP__ = """
Specify the nepho subcommand. Options include:
  "show-template", "validate-template", "show-params", "deploy", "delete".
"""

__DEPLOYMENT_HELP__= """
Specify the application deployment file to use. These are  stored in ./deployments/ as YAML files.
"""

__ENV_HELP__ = """
Specify the environment to use. 
Must be a section in the deplyoment file. 
Usually something like "development," testing", or "production."
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", type=str, help=__SUBCOMAMND_HELP__)
    parser.add_argument("deployment", type=str, help=__DEPLOYMENT_HELP__)
    parser.add_argument("-E", "--environment", type=str, help=__ENV_HELP__, default='development')
    parser.add_argument("-N", "--name", type=str, help="Specify a custom name for the application stack", default='')    
    parser.add_argument("--driver", type=str, help="Specify the orchestration driver", default='aws')    
    parser.add_argument("--aws", type=str, help="Specify a string to be passed through to the AWS driver", default='aws')
    parser.add_argument("--vagrant", type=str, help="Specify a string to be passed through to the Vagrant driver", default='')
    args = parser.parse_args()

    parsed = dict()
    parsed['subcommand'] = args.subcommand
    parsed['deployment']     = args.deployment       
    parsed['opts'] = dict()
    parsed['opts']['environment'] = args.environment
    parsed['opts']['name']        = args.name  
    parsed['opts']['driver']      = args.driver     
    if args.aws:
        parsed['opts']['aws'] = args.aws
    if args.vagrant:
        parsed['opts']['vagrant'] = args.vagrant
    return parsed
