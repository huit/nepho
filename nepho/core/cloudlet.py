# coding: utf-8
import os
from os import path
from tempfile import mkdtemp
from time import time
import re
import yaml
import requests
import glob
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
        self.defn = None
        if self.path is not None:
            try:
                self.defn = yaml.load(open(path.join(self.path, "cloudlet.yaml")))
            except Exception as e:
                print "Error loading cloudlet YAML file!"
                exit(1)
        
        # include metadata into the definition dictionary        
        self.defn['name'] = self.name
        self.defn['url'] = self.url
        
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
        blueprint_dir = path.join(self.path, "blueprints")
        blueprint_files = list()
        if path.isdir(blueprint_dir):
            blueprint_files.extend(glob.glob(path.join(blueprint_dir, '*.yaml')))
        else:
            return None
        
        blueprints = list()
        for f in blueprint_files:
            blueprints.append( blueprint.Blueprint(self, f) )
            
        return blueprints    
        
#def all_blueprints(self, name):
#    cloudlet = find_cloudlet(self, name)
#    blueprint_files = list()
#    if path.isdir(path.join(cloudlet, "blueprints")):
#        blueprint_files.extend(glob.glob(path.join(cloudlet, "blueprints", '*.yaml')))
#        return blueprint_files
#    else:
#        return None


#def find_blueprint(self, cloudlet, name):
#    blueprint_paths = all_blueprints(self, cloudlet)
#    paths = [path for path in blueprint_paths if name in path]
#    return paths[0]

        
    def clone(self, url):
        """
        Creates a local cloudlet as a git repo on disk
         from the supplied remote git URL.
        """
        try:
            temp_repo = mkdtemp()
            validate = Repo.init(temp_repo, bare=True)
            validate.git.ls_remote(url, heads=True)
        except Exception as e:
            print "Invalid or inaccessible remote repository URL."
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
        
    def archive(self, repo_name, archive_dir="/tmp"): 
        """Archives the cloudlet on disk as a tar file, and removes it."""
        repo = Repo(self.path)    
        try:
            print "Archiving %s to %s." % (repo_name, archive_dir)
            archive_file = path.join(archive_dir, "%s.tar") % (repo_name)
    
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
            if path.islink(self.path):
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
    """A class to manage cloudlets"""
    
    def __init__(self, config = None):
        self.config = config
        if self.config is not None:
            self.registry = self.config.get('cloudlet_registry_url')
            self.update_registry()
        

    def all_cloudlet_dirs(self):
        """Returns a list of paths to directories that contain cloudlets on disk."""
        dirs = self.config.get('cloudlet_dirs')
        return dirs
    
    def all_cloudlet_paths(self):
        """Returns a list of paths to cloudlets on disk."""
        dirs = self.config.get('cloudlet_dirs')
    
        # Collect the filesystem paths to every cloudlet into one list
        cloudlet_paths = list()
        for one_dir in dirs:
            cloudlet_paths.extend(glob.glob(path.join(one_dir, '*')))
    
        return cloudlet_paths
    
    def new(self, name, target_dir=None, url=None):
        """Create a new Cloudlet of a given name within a selected cloudlets dir, cloning from a URL."""
        if target_dir is None:
            target_dir = self.all_cloudlet_dirs()[0]

        cloudlet_path = path.join(target_dir, name)
        return Cloudlet(name, cloudlet_path, url)

        
    def find(self, name=None, multiple=False):
        """Search cloudlet locations for a cloudlet matching the given name, or all if name is None."""
        
        cloudlet_paths = self.all_cloudlet_paths()
        
        if name is None:
            paths = [path for path in cloudlet_paths ]
        else:
            paths = [path for path in cloudlet_paths if re.match(".*/"+name+"$", path) ]
        cloudlets = []
        for p in paths: cloudlets.append(Cloudlet(name,p))
        if len(cloudlets) == 0:
            return None
        if multiple is True:
            return cloudlets
        else:
            return cloudlets[0]
            
    def find_cloudlet_path(self, name, multiple=False):
        """Returns a list of paths to cloudlets based on the given name."""
        
        cloudlets = find(None, multiple)
        paths = [c.path for c in cloudlets]
        if multiple is True:
            return paths
        else:
            return paths[0]
    
    def list(self):
        """Returns a list of all cloudlets."""
        
        cloudlts = self.find(None, True)
        return cloudlts

    def update_registry(self):

        tmp_dir = self.config.get( 'tmp_dir')
        registry_cache = path.join(tmp_dir, "registry.yaml")
    
        # If the local registry is missing, empty, or stale (over 1 hour old)
        # update it from the configured URL. In either case, return the YAML object
        if not path.exists(registry_cache) or path.getsize(registry_cache) == 0 or (time() - path.getmtime(registry_cache)) > 3600:
            print "Updating cloudlet registry from: %s" % (self.registry)
            try:
                response = requests.get(self.registry, stream=True)
                with open(registry_cache, 'wb') as out_file:
                    copyfileobj(response.raw, out_file)
                    del response
            except Exception as e:
                print "Error updating cloudlet registry."
                print e
                exit(1)
    
            with open(registry_cache, 'r') as yaml_file:
                return yaml.load(yaml_file)
        else:
            with open(registry_cache, 'r') as yaml_file:
                return yaml.load(yaml_file)
   
    def get_registry(self):
        
        self.update_registry()
        tmp_dir = self.config.get('tmp_dir')
        registry_cache = path.join(tmp_dir, "registry.yaml")
        with open(registry_cache, 'r') as yaml_file:
            return yaml.load(yaml_file)        
        




