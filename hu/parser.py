import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("subcommand", type=str, help="Specify the hu subcommand")
    return parser.parse_args()
