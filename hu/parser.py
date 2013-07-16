import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", type=str, help="Specify the hu subcommand")
    parser.add_argument("-E", "--environment", type=str, help="Specify the environment", default='development')
    parser.add_argument("--aws", type=str, help="Specify a string to be passed through to the AWS driver", default='')
    parser.add_argument("--vagrant", type=str, help="Specify a string to be passed through to the Vagrant driver", default='')
    args = parser.parse_args()

    parsed = dict()
    parsed['subcommand'] = args.subcommand
    parsed['opts'] = dict()
    parsed['opts']['environment'] = args.environment
    if args.aws:
        parsed['opts']['aws'] = args.aws
    if args.vagrant:
        parsed['opts']['vagrant'] = args.vagrant
    return parsed
