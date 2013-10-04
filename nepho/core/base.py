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