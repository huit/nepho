import yaml
import glob
from pkg_resources import resource_filename
from os import listdir, environ, getenv
from os.path import isfile, isdir, join, expanduser, basename

def merge(user, system):
    if isinstance(user,dict) and isinstance(system,dict):
        for k,v in system.iteritems():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k],v)
    return user

# Return a list of the filesystem paths to all scenarios directories, with user
# scenarios listed *after* system scenarios (this is important for later
# merging).
def all_scenarios():
    system_scenarios_dir = resource_filename('nepho', 'data/scenarios')
    # If a user config dir is set use it, otherwise look in ~/.nepho
    user_config_dir      = getenv('NEPHO_CONFIG_DIR', join(expanduser("~"), ".nepho"))
    user_scenarios_dir   = join(user_config_dir, "scenarios")

    scenario_dirs = list()
    scenario_dirs.extend(glob.glob(join(system_scenarios_dir, '*')))
    if isdir(user_scenarios_dir):
        scenario_dirs.extend(glob.glob(join(user_scenarios_dir, '*')))
    return scenario_dirs

# Take multiple directory paths for the same scenario, find and read/validate
# each YAML file, and merge values, with later paths taking precedence. Return
# result as a dict.
def load_and_merge_scenario(paths):
    scenario = None
    for p in paths:
        scenario_key = basename(p)
        scenario_file = join(p, "%s.yaml") % (scenario_key)
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

# Find a scenario YAML file(s) and load into a hash
def find_scenario(name):
    scenario_dirs = all_scenarios()
    search = "%s" % join("scenarios", name)
    paths = [dir for dir in scenario_dirs if search in dir]

    return load_and_merge_scenario(paths)

# Load in all available scenarios, de-duplicate, merge, and return result as a
# dict
def load_and_merge_all_scenarios():
    scenario_dirs = all_scenarios()

    # Create a dict containing the name of each scenario and a list of all
    # its paths
    sall = dict()
    for sdir in scenario_dirs:
        skey = basename(sdir)
        if skey not in sall:
            sall[skey] = []
        sall[skey].append(sdir)

    # Iterate through the list and merge each scenario for display (costly but
    # what's a better option?)
    merged_scenarios = dict()
    for name, paths in sall.iteritems():
        merged_scenarios[name] = load_and_merge_scenario(paths)

    return merged_scenarios