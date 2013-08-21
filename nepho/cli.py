import argparse
from nepho.scenario import scenario_list, scenario_describe
from textwrap import TextWrapper

# debugging
from pprint import pprint

__all__ = ['command', 'parse_args']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.description = 'Simplified cloud orchestration tool for constructing virtual data centers'
    parser.add_argument("scenario",     type=str, help='An application deployment scenario configuration file, or "list" to show all available scenarios', default='')
    parser.add_argument("command",      type=str, nargs='?', help='One of: describe, create, delete, or debug', default='describe')
    parser.add_argument("-e", "--env",  type=str, help='Scenario environment (development, staging, etc.).  Most scenarios behave differently depending on their environment (default: development)', default=None)
    parser.add_argument("-n", "--name", type=str, help='A custom name for the created application stack, rather than the scenario\'s default name', default='')    
    parser.add_argument("-d", "--data", type=str, help='Additional command-line options to be passed to the scenario\'s driver (advanced usage only)', default='')    
    args = parser.parse_args()

    parsed = {
        'scenario':    args.scenario,
        'command':     args.command,
        'environment': args.env,
        'custom_name': args.name,
        'custom_data': args.data
    }
    return parsed

def command():
    args = parse_args()
    #pprint(args)
    scenario = args['scenario']
    command  = args['command']

    if scenario == 'list':
    	print "-"*80
    	print "Driver   Name                   Description"
    	print "-"*80
    	wrapper = TextWrapper(width=80, subsequent_indent="                                 ")
    	scenarios = scenario_list()
    	for k,v in scenario_list().items():
    		print wrapper.fill("%-7.7s  %-22.22s  %s" % (v['driver'], k, v['description']))
    	print "-"*80
    else:
    	if command == 'describe':
    		scenario_describe(scenario, args['environment'])
    	elif command == 'debug':
    		scenario_describe(scenario, args['environment'], debug=True)
    	else:
    		print "command is not describe, it is %s" % command
    return

    #subcmd = args['subcommand']
    #deployment  = args['deployment']
    ## FIXME: check to see whether we know of such a plugin
    #opts = dict( args['opts'] )
    #serialized = serialize(subcmd,deployment,opts)
    #return serialized