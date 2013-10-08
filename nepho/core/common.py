import glob
from os import listdir, environ, getenv, path

def all_cloudlets(self):
    dirs = list()
    dirs = self.config.get('global', 'cloudlets_path').split('\n')

    # Collect the filesystem paths to every cloudlet into one list
    cloudlet_paths = list()
    for c_dir in dirs:
        # If user-provided, expand any tildes in directory path
        c_dir_expanded = path.expanduser(c_dir)
        if path.isdir(c_dir_expanded):
            cloudlet_paths.extend(glob.glob(path.join(c_dir_expanded, '*')))

    return cloudlet_paths

def find_cloudlet(self, name):
    cloudlet_paths = all_cloudlets(self)
    paths = [path for path in cloudlet_paths if name in path]
    return paths[0]

def all_scenarios(self, name):
    cloudlet = find_cloudlet(self, name)
    scenario_files = list()
    if path.isdir(path.join(cloudlet, "scenarios")):
        scenario_files.extend(glob.glob(path.join(cloudlet, "scenarios", '*.yaml')))
        return scenario_files
    else:
        return None

def find_scenario(self, cloudlet, name):
    scenario_paths = all_scenarios(self, cloudlet)
    paths = [path for path in scenario_paths if name in path]
    return paths[0]