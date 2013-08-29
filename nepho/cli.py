import argparse
from os.path import basename
from nepho.display import display_scenario_list, display_scenario_description
from nepho.provider import call_provider

def parse_args():
    script = basename(__file__)
    providers = ['aws', 'heat', 'vagrant']
    actions = ['list', 'describe', 'show', 'clone', 'create', 'destroy']

    parser = argparse.ArgumentParser()
    parser.description = 'Simplified cloud orchestration tool for constructing virtual data centers'
    parser.add_argument("action",           type=str, help='Action to perform. Valid actions are: ' + ', '.join(actions), choices=actions, metavar='action')
    parser.add_argument("scenario",         type=str, nargs='?', help='An application deployment scenario. View all available scenarios by running \"%(prog)s list\".', default=None)
    parser.add_argument("-e", "--env",      type=str, help='Scenario environment (development, staging, etc.).  Most scenarios behave differently depending on their environment', default=None)
    parser.add_argument("-n", "--name",     type=str, help='A custom name for the created application stack, rather than the scenario\'s default name', default=None)    
    parser.add_argument("-p", "--provider", type=str, help='Override the default provider for a scenario. Valid providers are: ' + ', '.join(providers), default=None, choices=providers, metavar='PROVIDER')
    parser.add_argument("-d", "--data",     type=str, help='Additional action-line options to be passed to the scenario\'s provider (advanced usage only)', default=None)    
    args = parser.parse_args()

    # Some additional validation:
    # - Scenario is required unless action is list
    # - Environment is required if action is create, delete
    # - Provider is required if action is show
    if args.action != 'list' and args.scenario == None:
        parser.error("Please provide a scenario or run \"%s list\" to view all available scenarios." % (parser.prog))
    elif args.action in ['create', 'delete'] and args.env == None:
        parser.error("You must specify an environment (e.g. development). Run \"%s describe %s\" to see available environments" % (parser.prog, args.scenario))
    elif args.action in ['show'] and args.provider == None:
        parser.error("You must specify a provider (e.g. aws). Run \"%s describe %s\" to see available environments for this scenario" % (parser.prog, args.scenario))
    else:
        return {
            'action':      args.action,
            'scenario':    args.scenario,
            'environment': args.env,
            'custom_name': args.name,
            'custom_data': args.data,
            'name':        args.name,
            'provider':    args.provider
        }

def command():
    args = parse_args()
    action = args['action']

    if action == 'list':
        display_scenario_list(args['provider'])
    elif action == 'describe':
        display_scenario_description(args['scenario'], args['environment'])
    elif action == 'show':
        display_scenario_description(args['scenario'], args['environment'])
        call_provider(args['provider'], action, args['scenario'])
    elif action == 'clone':
        # Clone the scenario into .nepho/scenarios -- but what about the pattern?  do we need to know provider?
        print "need to clone"
    elif action in ['create', 'delete']:
        call_provider(args['provider'], action, args['scenario'])
    else:
        print "Invalid action!"
    return