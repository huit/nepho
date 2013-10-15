import glob
from os import listdir, environ, getenv, path

def all_cloudlets(self):
    dirs = list()
    dirs = self.config.get('nepho', 'cloudlet_dirs').split(',')

    # Collect the filesystem paths to every cloudlet into one list
    cloudlet_paths = list()
    for c_dir in dirs:
        c_dir.strip()
        # If user-provided, expand any tildes in directory path
        c_dir_expanded = path.expanduser(c_dir)
        if path.isdir(c_dir_expanded):
            cloudlet_paths.extend(glob.glob(path.join(c_dir_expanded, '*')))

    return cloudlet_paths

def find_cloudlet(self, name):
    cloudlet_paths = all_cloudlets(self)
    paths = [path for path in cloudlet_paths if name in path]
    return paths[0]

def all_blueprints(self, name):
    cloudlet = find_cloudlet(self, name)
    blueprint_files = list()
    if path.isdir(path.join(cloudlet, "blueprints")):
        blueprint_files.extend(glob.glob(path.join(cloudlet, "blueprints", '*.yaml')))
        return blueprint_files
    else:
        return None

def find_blueprint(self, cloudlet, name):
    blueprint_paths = all_blueprints(self, cloudlet)
    paths = [path for path in blueprint_paths if name in path]
    return paths[0]
