# coding: utf-8
import os
import jinja2
from copy import copy
from termcolor import colored

from nepho.core import provider_factory


class Scenario:
    """
    A scenario is an ephemeral amalgamation of a cloudlet blueprint, collected
    parameters, and the "live" filesystem, suitable for bringing up a stack.
    """

    def __init__(self, config, blueprint, params):
        self.config = config.to_dict()
        self.blueprint = blueprint
        self.transient_params = params

        self.cloudlet = self.blueprint.cloudlet
        self.provider_name = self.blueprint.provider_name

        pfactory = provider_factory.ProviderFactory()
        self.provider = pfactory.create(self.provider_name, config, self)

    @property
    def context(self):
        """
        Generates a context object to be injected into the templating engine.
        """

        # TODO: Make this compatible with the published cloudlet spec, i.e.
        # include params from the blueprint.yaml file as well as user-provided
        # params, both from local yaml files, prompting, and command line.

        self.context = dict()

        # Construct the parameters data structure
        # Order of precedence is (currently):
        # - Blueprint definition
        # - Stored params
        # - Transient params
        self.context['parameters'] = dict()
        if "parameters" in self.blueprint.definition:
            self.context['parameters'] = copy(self.blueprint.definition['parameters'])
        if "parameters" in self.config:
            for (k, v) in self.config['parameters'].items():
                self.context['parameters'][k] = v
        if self.transient_params is not None:
            for (k, v) in self.transient_params.items():
                self.context['parameters'][k] = v

        self.context['config'] = self.config

        if self.blueprint is not None:
            self.context['cloudlet'] = self.cloudlet.definition
            self.context['blueprint'] = self.blueprint.definition

        #
        # Temporary measure for backwards compat
        #
        self.context['scripts'] = None

        return self.context

    @property
    def template(self):
        """
        Load a blueprint template, generate a context, and return the rendered
        Jina2 template.
        """

        # Templates may be composed of multiple files in the template_path
        # location as well as a provider-specific common template location
        template_path = os.path.join(
            self.cloudlet.path, 'resources', self.blueprint.name,
            self.provider.TEMPLATE_FILENAME)
        template_common_dir = os.path.join(
            self.cloudlet.path, 'resources', 'common', self.provider.PROVIDER_ID)

        template_filename = os.path.basename(template_path)
        template_dirs = [template_common_dir, os.path.dirname(template_path)]

        # Initialize Jinja2
        jinjaFSloader = jinja2.FileSystemLoader(template_dirs)
        jinja_env = jinja2.Environment(loader=jinjaFSloader)
        jinja_template = jinja_env.get_template(template_filename)

        # Render the template
        self.template = None
        try:
            self.template = jinja_template.render(self.context)
        except jinja2.TemplateNotFound as e:
            print colored('Error: ', 'red') + 'could not find template file "%s"' % (e)
            print "Template search path is:"
            for dir in template_dirs:
                print "    " + dir
            exit(1)

        return self.template
