from nepho import scenario
from pprint import pprint
from textwrap import TextWrapper

def display_scenario_list(provider=None):
    scenarios = scenario.load_and_merge_all_scenarios()
    print "-"*80
    print "Name                    Description"
    print "-"*80
    wrapper = TextWrapper(width=80, subsequent_indent="                        ")
    for k,v in scenarios.items():
        if provider in v['providers'] or provider == None:
            print wrapper.fill("%-22.22s  %s" % (k, v['description']))
    print "-"*80
    print "Run \"nepho describe\" for more info on a specific scenario.\n"
    return

# Print a nicely formatted overview of a given scenario, optionally limited to
# a single environment.  If called in debug mode, also load in the scenario's
# pattern from the provider and display user parameters and the complete
# provider debug output.
def display_scenario_description(name, environment=None, debug=None):
    s = scenario.find_scenario(name)
    wrapper = TextWrapper(width=80, subsequent_indent="             ")

    print "-"*80
    print "Name:        %s" % (name)
    print "Providers:   %s (default: %s)" % (", ".join(s['providers']), s['default_provider'])
    print wrapper.fill("Description: %s" % (s['description']))
    print "-"*80

    s = s.pop('stages', None)
    
    if environment != None:
        print "Scenario configuration [%s]:\n" % (environment)
        s = s.pop(environment, None)
    else:
        print "Scenario configuration:\n"

    pprint(s)

    print "-"*80
    return