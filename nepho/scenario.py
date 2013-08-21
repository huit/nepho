# List, load, and view scenario configurations
import yaml
import glob
from pkg_resources import resource_filename
from os import listdir, environ, getenv
from os.path import isfile, isdir, join, expanduser, basename
from pprint import pprint
from textwrap import TextWrapper

def merge(user, system):
    if isinstance(user,dict) and isinstance(system,dict):
        for k,v in system.iteritems():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k],v)
    return user

# Return a list of the filesystem paths to all scenarios directories, with user
# scenarios listed *after* system scenarios
def scenario_find_all():
    # If a user config dir is set use it, otherwise look in ~/.nepho
    user_config_dir      = getenv('NEPHO_CONFIG_DIR', join(expanduser("~"), ".nepho"))
    user_scenarios_dir   = join(user_config_dir, "scenarios")
    system_scenarios_dir = resource_filename('nepho', 'data/scenarios')
    scenario_dirs = list()
    scenario_dirs.extend(glob.glob(join(system_scenarios_dir, '*')))
    if isdir(user_scenarios_dir):
        scenario_dirs.extend(glob.glob(join(user_scenarios_dir, '*')))
    return scenario_dirs

def scenario_load_and_merge(paths):
    scenario = None
    for p in paths:
        scenario_key = basename(p)
        scenario_file = join(p, "%s.yaml") % scenario_key
        if isfile(scenario_file):
            try:
                scenario_yaml = yaml.safe_load(open(scenario_file))
            except IOError as e:
                print "Error loading or parsing deployment scenario file \"%s\"" % (scenario_file)
                print e
                sys.exit(1)
            if scenario != None:
                scenario = merge(scenario_yaml, scenario)
            else:
                scenario = scenario_yaml
    return scenario

def scenario_list():
    scenario_dirs = scenario_find_all()
    scenarios = dict()
    for sdir in scenario_dirs:
        skey = basename(sdir)
        sfile = join(sdir, "%s.yaml") % skey
        if isfile(sfile):
            syaml = yaml.safe_load(open(sfile))
            try:
                new_scenario = {
                    'description': syaml['description'],
                    'driver':      syaml['driver']
                }
            except KeyError as err:
                err.args = ("YAML scenario file is missing a required key/value pair",)
                raise

            if skey in scenarios:
                scenarios[skey] = merge(new_scenario, scenarios[skey])
            else:
                scenarios[skey] = new_scenario

    return scenarios

def scenario_describe(name, environment=None, debug=None):
    scenario_dirs = scenario_find_all()
    search = "%s" % join("scenarios", name)
    paths = [dir for dir in scenario_dirs if search in dir]

    s = scenario_load_and_merge(paths)

    wrapper = TextWrapper(width=80, subsequent_indent="             ")

    print "-"*80
    print "Name:        %s" % (name)
    print "Driver:      %s" % (s['driver'])
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
    print "Pattern parameters:"
    # print cf json parameters (or pp list)
    print "-"*80
    if debug == True:
        print "Pattern configuration:"
        # find driver in yaml, load and call driver.describe or similar
        print "-"*80
    return

def scenario_load(name):
    return