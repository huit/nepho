# coding: utf-8
import yaml
import requests
from nepho.core import common
from os import path
from shutil import rmtree, copyfileobj
from termcolor import colored
from time import time
from git import *

def list_all_cloudlets(self):
    all_cloudlets = common.all_cloudlets(self)
    dir = ""
    items = list()
    for cloudlet in sorted(all_cloudlets):
        # Print directory if it changes
        if dir != path.dirname(cloudlet):
            dir = path.dirname(cloudlet)
            print colored(dir, "cyan")
        name = path.basename(cloudlet)

        # If there are multiple versions of a cloudlet with the same name,
        # subsequent versions will be ignored by other commands
        if name not in items:
            try:
                y = yaml.load(open(path.join(cloudlet, 'cloudlet.yaml')))
            except:
                print colored("└──", "yellow"), name, "(", colored("error", "red"), "- missing or malformed cloudlet.yaml )"
            else:
                print colored("└──", "yellow"), name, "(", colored("v%s", "blue") % (y['version']), ")"
            items.append(name)
        else:
            print colored("└──", "yellow"), name, "(", colored("error", "red"), "- duplicate cloudlet will be ignored )"
    return

def cloudlet_registry(self):
    registry = self.config.get('nepho', 'cloudlet_registry_url')
    cache_dir = self.config.get('nepho', 'cache_dir')
    registry_cache = path.join(cache_dir, "registry.yaml")

    # If the local registry is missing, empty, or stale (over 1 hour old)
    # update it from the configured URL. In either case, return the YAML object
    if not path.exists(registry_cache) or path.getsize(registry_cache) == 0 or (time() - path.getmtime(registry_cache)) > 3600:
        print "Updating cloudlet registry from: %s" % (registry)
        try:
            response = requests.get(registry, stream=True)
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

def clone_cloudlet(self, url, repo_path):
    repo = Repo.init(repo_path, bare=True)
    repo.create_remote('origin', url)
    repo.remotes.origin.pull()
    repo.submodule_update(init=True)

def update_cloudlet(self, repo_path):
    repo = Repo(repo_path)
    repo.remotes.origin.pull()
    repo.submodule_update()

def archive_cloudlet(self, repo_path):
    archive_dir = self.config.get('nepho', 'archive_dir')
    repo_name = path.basename(repo_path)
    repo = Repo(repo_path)
    repo.archive(open(path.join(archive_path, "%(repo_name).tar"),'w'))
    rmtree(repo_path)
