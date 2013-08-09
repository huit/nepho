import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", type=str, help="Specify the nepho subcommand")
    parser.add_argument("deployment", type=str, help="Specify the application and pattern to deploy")
    parser.add_argument("-E", "--environment", type=str, help="Specify the environment", default='development')
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
