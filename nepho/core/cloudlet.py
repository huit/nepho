# coding: utf-8
import os
import sys
import tempfile
from time import time
import re
import yaml
import requests
import glob
from termcolor import colored
from shutil import rmtree, copyfileobj

from git import Repo

from nepho.core import common, blueprint


class Cloudlet:
    """A class that encompasses a cloudlet"""

    def __init__(self, name, cloudlet_path=None, url=None):
        self.path = cloudlet_path
        self.url = url
        self.name = name

        # If specified initialize this from a remote repo
        if url is not None:
            self.clone(url)

        # now load definition, and fail is unable
        self.definition = None
        if self.path is not None:
            try:
                self.definition = yaml.safe_load(open(os.path.join(self.path, "cloudlet.yaml")))
            except Exception:
                print "Error loading cloudlet YAML file!"
                exit(1)

        # include metadata into the definition dictionary
        self.definition['name'] = self.name
        self.definition['url'] = self.url
        self.definition['path'] = self.path

    def serialize(self):
        """Returns the cloudlets data definition as a JSON string."""

    def blueprint(self, name):
        """Return a blueprint by name."""
        bps = self.blueprints()
        for bp in bps:
            if bp.name == name:
                return bp

    def blueprints(self):
        """Returns a list of blueprints."""
        blueprint_dir = os.path.join(self.path, "blueprints")
        blueprint_files = list()
        if os.path.isdir(blueprint_dir):
            blueprint_files.extend(glob.glob(os.path.join(blueprint_dir, '*.yaml')))
        else:
            return None

        blueprints = list()
        for f in blueprint_files:
            blueprints.append(blueprint.Blueprint(self, f))

        return blueprints

    def clone(self, url):
        """
        Creates a local cloudlet as a git repo on disk
         from the supplied remote git URL.
        """
        try:
            temp_repo = tempfile.mkdtemp()
            validate = Repo.init(temp_repo, bare=True)
            validate.git.ls_remote(url, heads=True)
        except Exception as e:
            print colored("Error: ", "red") + "Invalid or inaccessible remote repository URL.\n"
            print e
            exit(1)
        else:
            try:
                repo = Repo.clone_from(url, self.path)
                repo.submodule_update(init=True)
            except Exception as e:
                print "Cloudlet install failed."
                print e
                exit(1)
            else:
                print "Cloudlet installed: %s" % (self.path)
        finally:
            rmtree(temp_repo)

    def update(self):
        """Update the local cloudlet git repo on disk from any origin."""

        print "Updating cloudlet: %s" % (self.path)
        repo = Repo(self.path)
        repo.remotes.origin.pull()
        repo.submodule_update()

    def publish(self):
        """Update the remote cloudlet git repo from the local one."""

        print "Publishing cloudlet: %s" % (self.path)
        repo = Repo(self.path)
        repo.remotes.origin.push()

    def archive(self, repo_name, archive_dir=tempfile.gettempdir()):
        """Archives the cloudlet on disk as a tar file, and removes it."""
        repo = Repo(self.path)
        try:
            print "Archiving %s to %s." % (repo_name, archive_dir)
            archive_file = os.path.join(archive_dir, "%s.tar") % (repo_name)

            # TODO: If a tar already exists, rotate/increment it. I tried using
            # logging.handlers.RotatingFileHandler for this, but it didn't quite
            # work (gave zero-length files).

            # Archive and delete the repository
            repo.archive(open(archive_file, "w"))
        except Exception as e:
            print "Archive failed -- aborting!"
            print e
            exit(1)
        else:
            if os.path.islink(self.path):
                os.unlink(self.path)
            else:
                rmtree(self.path)

    def uninstall(self):
        """Meant to remove the cloudlet from disk. For now a no-op."""
        # No-op here ... done by archive above for now
        pass

    def get_path(self):
        """Return the  path to the cloudlet's root dir."""
        return self.path


class CloudletManager:
    """A class to create, lookup, and manage cloudlets"""

    def __init__(self, app_obj):
        self.cloudlet_dirs  = app_obj.cloudlet_dirs
        self.registry       = app_obj.config.get('nepho', 'cloudlet_registry_url')
        self.cache_dir      = app_obj.config.get('nepho', 'cache_dir')
        self.registry_cache = os.path.join(self.cache_dir, "registry.yaml")
        self.update_registry()

    def all_cloudlet_dirs(self):
        """Returns a list of paths to directories that contain cloudlets on disk."""
        return self.cloudlet_dirs

    def all_cloudlet_paths(self):
        """Returns a list of paths to cloudlets on disk."""
        cloudlet_paths = list()
        for dir in self.cloudlet_dirs:
            cloudlet_paths.extend(glob.glob(os.path.join(dir, '*')))
        return cloudlet_paths

    def new(self, name, target_dir=None, url=None):
        """Create a new Cloudlet of a given name within a selected cloudlets dir, cloning from a URL."""
        if target_dir is None:
            target_dir = self.all_cloudlet_dirs()[0]

        cloudlet_path = os.path.join(target_dir, name)
        return Cloudlet(name, cloudlet_path, url)

    def find(self, name=None, multiple=False):
        """Search cloudlet locations for a cloudlet matching the given name, or all if name is None."""

        cloudlet_paths = self.all_cloudlet_paths()

        if name is None:
            paths = [path for path in cloudlet_paths]
        else:
            paths = [path for path in cloudlet_paths if (os.path.split(path))[1] == name]
        cloudlets = []
        for p in paths:
            cloudlets.append(Cloudlet(name, p))
        if len(cloudlets) == 0:
            return None
        if multiple is True:
            return cloudlets
        else:
            return cloudlets[0]

    def find_cloudlet_path(self, name, multiple=False):
        """Returns a list of paths to cloudlets based on the given name."""

        cloudlets = self.find(None, multiple)
        paths = [c.path for c in cloudlets]
        if multiple is True:
            return paths
        else:
            return paths[0]

    def list(self):
        """Returns a list of all cloudlets."""

        cloudlts = self.find(None, True)
        return cloudlts

    def clear_registry(self):
        """Removes any cached registry info in the local nepho directory."""
        try:
            os.remove(self.registry_cache)
        except Exception:
            pass

    def update_registry(self):
        """Pulls down a fresh copy of the cloudlet registry."""

        # If the local registry is missing, empty, or stale (over 4 hours old)
        # update it from the configured URL. In either case, return the YAML object
        if not os.path.exists(self.registry_cache) or os.path.getsize(self.registry_cache) == 0 or (time() - os.path.getmtime(self.registry_cache)) > 14400:
            print "Updating cloudlet registry from: %s" % (self.registry)
            try:
                response = requests.get(self.registry, stream=True)
                with open(self.registry_cache, 'wb') as out_file:
                    yaml.safe_dump(yaml.safe_load(response.raw), out_file, default_flow_style=True)
                    del response
            except yaml.YAMLError, detail:
                print "Invalid registry data received: ", detail
                pass
            except IOError:
                print "Error updating cloudlet registry. Using last cached version.\n"
                pass

            with open(self.registry_cache, 'r') as yaml_file:
                try:
                    return yaml.safe_load(yaml_file)
                except yaml.YAMLError, detail:
                    print "Invalid registry data found: ", detail
                    print "Try running the nepho command again.\n"
                    os.unlink(self.registry_cache)
                    sys.exit(1)
        else:
            with open(self.registry_cache, 'r') as yaml_file:
                try:
                    return yaml.safe_load(yaml_file)
                except yaml.YAMLError, detail:
                    print "Invalid registry data found: ", detail
                    print "Try running the nepho command again.\n"
                    os.unlink(self.registry_cache)
                    sys.exit(1)

    def get_registry(self):
        """Returns a dictionary with registry values."""
        self.update_registry()
        with open(self.registry_cache, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
