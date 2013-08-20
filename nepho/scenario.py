# List, load, and view scenario configurations
import yaml
import glob
from os import listdir, environ
from os.path import isfile, isdir, join, expanduser
from pprint import pprint

# Return a list of the filesystem paths to all scenarios directories, with user
# scenarios listed *after* system scenarios
def find_all():
    # If a user config dir is set use it, otherwise look in ~/.nepho
    user_config_dir      = getenv('NEPHO_CONFIG_DIR', join(expanduser("~"), ".nepho"))
    user_scenarios_dir   = join(user_config_dir, "scenarios")
    system_scenarios_dir = resource_filename('nepho', 'data/scenarios')
    scenarios = list()
    scenarios.extend(glob.glob(join(system_scenarios_dir, '*')))
    if isdir(user_scenarios_dir):
        scenarios.extend(glob.glob(join(user_scenarios_dir, '*')))
    return scenarios

def find_and_merge(scenario):

def list():
    scenario_dirs = find_all()
    scenarios = list()
    for sd in scenario_dirs:
        sf = join(sd, "%s.yaml") % basename(sd)
        if isfile(sf):
            sy = yaml.safe_load(open(sf))
            scenarios.append(dict(
                ('key', basename(sd)),
                ('name', sy['name']),
                ('dsecription', sy['description']),
                ('driver', sy['driver'])
            ))

    # find_all
    # parse
    # display

def describe(scenario):
    # pprint(yaml)
    # pp cf parameters???
    # output structured yaml of a scenario?  or just description?

def load(scenario):
    #stuff