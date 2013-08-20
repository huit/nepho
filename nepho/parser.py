import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario",     type=str, help='An application deployment scenario configuration file, or "list" to show all available scenarios', default='')
    parser.add_argument("command",      type=str, help='One of: describe, create, delete, or debug', default='')
    parser.add_argument("-e", "--env",  type=str, help='Scenario environment (development, staging, etc.).  Most scenarios behave differently depending on their environment (default: development)', default='development')
    parser.add_argument("-n", "--name", type=str, help='A custom name for the created application stack, rather than the scenario\'s default name', default='')    
    parser.add_argument("-d", "--data", type=str, help='Additional command-line options to be passed to the scenario\'s driver (advanced usage only)', default='')    
    args = parser.parse_args()

    parsed = dict(
        ('scenario',    args.scenario),
        ('command',     args.command ),
        ('environment', args.env     ),
        ('custom_name', args.name    ),
        ('custom_data', args.data    )
    )
    return parsed