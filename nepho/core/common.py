import glob
from os import path


def all_cloudlets(self):
    dirs = list()
    dirs = self.config.get('nepho', 'cloudlet_dirs').split(',')

    # Collect the filesystem paths to every cloudlet into one list
    cloudlet_paths = list()
    for one_dir in dirs:
        # If user-provided, expand any tildes in directory path
        one_dir = path.expanduser(one_dir.strip())
        if path.isdir(one_dir):
            cloudlet_paths.extend(glob.glob(path.join(one_dir, '*')))

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
