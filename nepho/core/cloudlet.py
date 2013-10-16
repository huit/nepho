# coding: utf-8
import yaml
import requests
from nepho.core import common
from os import path
from shutil import rmtree, copyfileobj
from termcolor import colored
from textwrap import TextWrapper
from tempfile import mkdtemp
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
            repo = Repo.clone_from(url, repo_path)
            repo.submodule_update(init=True)
        except Exception as e:
            print "Cloudlet install failed."
            print e
            exit(1)
        else:
            print "Cloudlet installed: %s" % (repo_path)
    finally:
        rmtree(temp_repo)

def update_cloudlet(self, repo_path):
    print "Updating cloudlet: %s" % (repo_path)
    repo = Repo(repo_path)
    repo.remotes.origin.pull()
    repo.submodule_update()

def archive_cloudlet(self, repo_name, repo_path):
    archive_dir = self.config.get('nepho', 'archive_dir')
    repo = Repo(repo_path)

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
        rmtree(repo_path)

def describe_cloudlet(self, name):
    try:
        repo_path = common.find_cloudlet(self, name)
    except:
        print "Invalid cloudlet name provided."
        exit(1)

    try:
        y = yaml.load(open(path.join(repo_path, "cloudlet.yaml")))
    except:
        print "Error loading cloudlet YAML file!"
        exit(1)

    wrapper = TextWrapper(width=80, subsequent_indent="              ")

    print "-"*80
    print "Name:         %s" % (y['name'])
    print "Version:      %s" % (y['version'])
    print "Author:       %s" % (y['author'])
    print "License:      %s" % (y['license'])
    print wrapper.fill("Summary:      %s" % (y['summary']))
    print wrapper.fill("Description:  %s" % (y['description']))
    print "-"*80
    return
