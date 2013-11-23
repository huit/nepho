import glob
import os


class cwd:
    """
    Context manager for changing the current working directory

    with cwd("foobar"):
        do a thing
    """
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def merge(user, system):
    """
    Merge two dicts, user and system, recursively, with user taking precedence.
    """
    if isinstance(user, dict) and isinstance(system, dict):
        for k, v in system.iteritems():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k], v)
    return user


def select_list(self, items_list=[], all=False, desc="Select an item:"):
    """
    Return the item selected by the user, or, optionally, "all".  If there is
    only one list item, return it without prompting.
    """
    if items_list == []:
        return
    elif len(items_list) == 1:
        return items_list[0]
    else:
        item_incr = 0
        print ""
        for one_item in items_list:
            item_incr += 1
            print "  %d) %s" % (item_incr, one_item.strip())
        if all is True:
            print "  0) All"
        user_item = int()
        try:
            user_item = input("\n%s [1]: " % (desc))
        except NameError:
            # User did not input a number
            user_item = -1
        except SyntaxError:
            # User accepted default
            user_item = 1

        if user_item == 0 and all is True:
            return items_list
        elif user_item <= item_incr and user_item > 0:
            return items_list[user_item - 1]
        else:
            print "Invalid selection, please select a number from the list."
            exit(1)


def all_cloudlets(self):
    # Collect the filesystem paths to every cloudlet into one list
    cloudlet_paths = list()
    for one_dir in self.cloudlet_dirs:
        cloudlet_paths.extend(glob.glob(os.path.join(one_dir, '*')))

    return cloudlet_paths


def find_cloudlet(self, name, multiple=False):
    cloudlet_paths = all_cloudlets(self)
    paths = [path for path in cloudlet_paths if name in path]
    if multiple is True:
        return paths
    else:
        return paths[0]


def all_blueprints(self, name):
    cloudlet = find_cloudlet(self, name)
    blueprint_files = list()
    if os.path.isdir(os.path.join(cloudlet, "blueprints")):
        blueprint_files.extend(glob.glob(os.path.join(cloudlet, "blueprints", '*.yaml')))
        return blueprint_files
    else:
        return None


def find_blueprint(self, cloudlet, name):
    blueprint_paths = all_blueprints(self, cloudlet)
    paths = [path for path in blueprint_paths if name in path]
    return paths[0]
