# coding: utf-8

from os import path
import yaml
from nepho.core import common


class Pattern:
    """An infrastructure design pattern class"""

    def __init__(self, name, pattern_file=None):
        self.name = name
        self.template = pattern_file

        self.provider = None
        self.context = dict()
        self.template_dirs = list()

    def set_provider(self, p):
        self.provider = p

    def set_context(self, c):
        self.context = c

    def get_context(self):
        return self.context

    def get_template_file(self):
        return self.template

    def render(self):
        pass
