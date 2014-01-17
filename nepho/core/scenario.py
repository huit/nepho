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

    def __init__(self, blueprint, stored_params, user_params, name):
        self.blueprint = blueprint
        self.stored_params = stored_params.to_dict()
        self.user_params = user_params
        self.name = name

        self.cloudlet = self.blueprint.cloudlet
        self.provider_name = self.blueprint.provider_name

        pfactory = provider_factory.ProviderFactory()
        self.provider = pfactory.create(self.provider_name, self.stored_params, self)

    @property
    def context(self):
        """
        Generates a context object to be injected into the templating engine.
        """
        self.context = dict()
        self.context['parameters'] = dict()

        # Inheritance is Provider -> Cloudlet -> Blueprint -> Stored -> User
        # Only parameters defined by the provider, cloudlet, or blueprint are
        # passed into the context, even if they are stored or passed by the user.
        if self.provider.params is not None:
            for (k, v) in self.provider.params.items():
                self.context['parameters'][k] = v
        if "parameters" in self.cloudlet.definition:
            try:
                for (k, v) in self.cloudlet.definition['parameters'].items():
                    self.context['parameters'][k] = v
            except:
                pass
        if "parameters" in self.blueprint.definition:
            try:
                for (k, v) in self.blueprint.definition['parameters'].items():
                    self.context['parameters'][k] = v
            except:
                pass

        if self.stored_params is not None:
            try:
                for (k, v) in self.stored_params.items():
                    if k in self.context['parameters']:
                        self.context['parameters'][k] = v
            except:
                pass
        if self.user_params is not None:
            try:
                for (k, v) in self.user_params.items():
                    if k in self.context['parameters']:
                        self.context['parameters'][k] = v
            except:
                pass

        # Provide a limited/cleaned set of values from cloudlet.yaml and blueprint.yaml
        if self.blueprint is not None:
            c = self.cloudlet.definition
            b = self.blueprint.definition

            self.context['cloudlet'] = {
                'name': c['name'],
                'format': c['format'],
                'path': c['path'],
                'version': c['version'],
            }
            self.context['blueprint'] = {
                'name': b['name'],
                'provider': b['provider'],
            }

            # Backwards compatibility
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
