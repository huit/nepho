# coding: utf-8
from nepho.core import resource, context


class AbstractProvider:
    """An abstract infrastructure provider class."""

    def __init__(self, config, scenario=None):
        self.config = config
        self.scenario = scenario

        self.resourceManager = resource.ResourceManager(self.config)
        self.context = context.Context(self.config)

    def validate_template(self, template):
        pass

    def format_template(self, template):
        return template

    def deploy(self):
        pass

    def status(self):
        pass

    def access(self):
        pass

    def destroy(self):
        pass
