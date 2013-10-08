# Merge two dicts, user and system, recursively, with user taking precedence
def merge(user, system):
    if isinstance(user,dict) and isinstance(system,dict):
        for k,v in system.iteritems():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k],v)
    return user

# Take multiple directory paths for the same scenario, find and read/validate
# each YAML file, and merge them, with later paths taking precedence. Return
# result as a dict.
def load_and_merge_scenario(paths):
    scenario = None
    for p in paths:
        scenario_key = basename(p)
        scenario_file = join(p, "%s.yaml") % (scenario_key)
        if isfile(scenario_file):
            try:
                f = open(scenario_file)
                scenario_yaml = yaml.safe_load(f)
                f.close()
            except IOError as e:
                print "Error loading or parsing deployment scenario file \"%s\"" % (scenario_file)
                print e
                exit(1)
            if scenario != None:
                scenario = merge(scenario_yaml, scenario)
            else:
                scenario = scenario_yaml
    return scenario
