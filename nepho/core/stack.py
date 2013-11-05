

# Take multiple directory paths for the same blueprint, find and read/validate
# each YAML file, and merge them, with later paths taking precedence. Return
# result as a dict.
def load_and_merge_blueprint(paths):
    blueprint = None
    for p in paths:
        blueprint_key = basename(p)
        blueprint_file = join(p, "%s.yaml") % (blueprint_key)
        if isfile(blueprint_file):
            try:
                f = open(blueprint_file)
                blueprint_yaml = yaml.safe_load(f)
                f.close()
            except IOError as e:
                print "Error loading or parsing deployment blueprint file \"%s\"" % (blueprint_file)
                print e
                exit(1)
            if blueprint != None:
                blueprint = merge(blueprint_yaml, blueprint)
            else:
                blueprint = blueprint_yaml
    return blueprint
