# coding: utf-8
import yaml
from nepho.core import common, pattern
from os import path


class Blueprint:
    """A simple example class"""

    def __init__(self, cloudlt, blueprint_file):

        self.file = blueprint_file
        self.cloudlet = cloudlt

        # now load definition, and fail is unable
        self.defn = None
        if self.file is not None:
            try:
                self.defn = yaml.load(open(blueprint_file))
            except Exception as e:
                print "Error loading blueprint YAML file at %s!" % (blueprint_file)
                print e
                exit(1)
        self.name = path.basename(blueprint_file).replace(".yaml", "")
        self.defn['name'] = self.name
        self.provider_name = self.defn['provider']
        self.validate()

    def validate(self):
        """Validates the blueprint as defined to determine if it's sufficent and properly formed."""

        # If a name isn't specified, our name is the blueprint's name
        if not "pattern" in self.defn or self.defn['pattern'] is None:
            self.defn['pattern'] = self.name

        fields = ["provider"]
        for f in fields:
            if not f in self.defn.keys():
                print "Blueprint is missing required field %s." % (f)
                exit(1)

    def cloudlet(self):
        """Return the cloudlet that this blueprint is part of."""
        return self.cloudlet

    def pattern(self):
        """Returns a pattern object that represents the pattern in the blueprint."""
        patternString = self.defn['pattern']
        pattrn = pattern.Pattern(patternString)
        return pattrn
