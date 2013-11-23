# coding: utf-8


class AbstractProvider:
    """An abstract infrastructure provider class."""

    def __init__(self, config, scenario=None):
        self.config = config
        self.scenario = scenario
        self.params = None

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
