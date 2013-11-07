# coding: utf-8
import copy


class Context:
    """
    Produce a context dictionary for use with the Jinja2 templating engine. It
    contains cloudlet.yaml content, blueprint.yaml content, parameters, and
    all nepho config values.
    """

    def __init__(self, cfgMgr):
        self.configManager = cfgMgr
        self.blueprint = None
        self.transient_params = dict()

    def add_params(self, params):
        self.transient_params = params

    def generate(self):
        """Generates a context object to be injected into the templating engine."""

        context = dict()
        config = self.configManager.to_dict()

        # TODO: Make this compatible with the published cloudlet spec, i.e.
        # include params from the blueprint.yaml file as well as user-provided
        # params, both from local yaml files, prompting, and command line.

        # construct the parameters data structure
        context['parameters'] = dict()
        if "parameters" in config:
            context['parameters'] = copy.copy(config['parameters'])
        if self.transient_params is not None:
            for (k, v) in self.transient_params.items():
                context['parameters'][k] = v

        context['config'] = config

        if self.blueprint is not None:
            cloudlt = self.blueprint.cloudlet
            context['cloudlet'] = cloudlt.defn
            context['blueprint'] = self.blueprint.defn

        #
        # Temporary measure for backwards compat
        #
        context['scripts'] = None

        return context
