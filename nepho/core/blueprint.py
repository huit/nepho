# coding: utf-8
import yaml
import os

from nepho.core import common


class Blueprint:
    def __init__(self, cloudlet, blueprint_file):
        self.file = blueprint_file
        self.cloudlet = cloudlet

        # now load definition, and fail is unable
        self.definition = None
        if self.file is not None:
            try:
                self.definition = yaml.load(open(self.file))
            except Exception as e:
                print "Error loading blueprint YAML file at %s!" % (self.file)
                print e
                exit(1)
        self.name = os.path.basename(os.path.splitext(self.file)[0])
        self.definition['name'] = self.name
        self.provider_name = self.definition['provider']
        self.validate()

    def validate(self):
        """Validates the blueprint as defined to determine if it's sufficent and properly formed."""
        fields = ["provider"]
        for f in fields:
            if not f in self.definition.keys():
                print "Blueprint is missing required field %s." % (f)
                exit(1)
