# coding: utf-8
import yaml
from nepho.core import common


class ParamsManager:
    """
    Manage a hierarchal set of parameters that provide the context for
    launching a scenario.
    """

    """
    Future Planning...

    params.StackPrefix = 'dsilverman'
    params.aws.Region = 'us-east-1'
    params.get_context('aws.huit-mediawiki.development')

    param.set('aws.Region', 'us-east-1')
    param.get('aws.Region')

    params.StackPrefix
    params.aws.Region
    params.aws.huit-mediawiki.InstanceType
    params.aws.huit-mediawiki.development.UpdatePackages

    StackPrefix: dsilverman
    aws:
        Region: us-east-1
        huit-mediawiki:
            InstanceType: t1.micro
            development:
                UpdatePackages: False
    """

    def __init__(self, app_obj):
        self.params_file = app_obj.app.config.get('nepho', 'params_file')
        self.params = dict()
        self.load()

    def keys(self):
        return self.params.keys()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError:
            return None

    def set(self, key, value):
        self.params[key] = value
        self.save()

    def unset(self, key):
        try:
            del self.params[key]
        except KeyError:
            pass
        self.save()

    def to_dict(self):
        return self.params

    def load(self):
        """Load parameters into a dict from YAML params_file"""
        try:
            with open(self.params_file, "r") as file:
                self.params = yaml.load(file)
        except Exception:
            pass

    def save(self):
        """Save current parameters into YAML params_file"""
        try:
            with open(self.params_file, "wb") as file:
                yaml.dump(self.params, file)
        except Exception as e:
            print "Error writing parameters to file %s!" % (self.params_file)
            print e
            exit(1)
