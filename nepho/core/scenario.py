# coding: utf-8
from nepho.core import pattern, resource, context, provider_factory


class Scenario:
    """
    A class that encapsulates a blueprint with an actual parameter and config environment.

    The class is intended to be assembled, then handed off to other objects that
      need access to the overall state of the request.

    """

    def __init__(self, config, bprint, params):
        self.config = config
        self.blueprint = bprint
        self.transient_params = params

        self.cloudlet = self.blueprint.cloudlet
        self.provider_name = self.blueprint.provider_name

        pfac = provider_factory.ProviderFactory()
        self.provider = pfac.create(self.provider_name, config, self)

        self.remgr = resource.ResourceManager(config)
        self.context = context.Context(config)
        self.context.blueprint = self.blueprint
        self.context.add_params(params)

        self.pattern = None

    def get_context(self):
        """Generate a context for this scenario."""
        return self.context.generate()

    def get_template(self):
        """Return a generated template file for this blueprint and these params & configs."""
        template_string = self.remgr.render_template(self)
        return self.provider.format_template(template_string)

    def get_pattern(self):
        """Loads in a blueprint, looks up the pattern, and configures the context."""
        if self.pattern is None:
            pattern_str = self.blueprint.pattern()
            pattern_file = self.remgr.lookup_pattern_file(self.blueprint, self.provider)
            self.pattern = pattern.Pattern(pattern_str, pattern_file)
            self.pattern.set_provider(self)
        return self.pattern

#     def validate(self):
#         """Validates the blueprint as defined to determine if it's sufficent and properly formed."""
#
#         # If a name isn't specified, our name is the blueprint's name
#         if not "pattern" in self.defn or self.defn['pattern'] is None:
#             self.defn['pattern'] = self.name
#
#         fields = ["provider" ]
#         for f in fields:
#             if not f in self.defn.keys():
#                 print "Blueprint is missing required field %s." % (f)
#                 exit(1)
#
#     def cloudlet(self):
#         """Return the cloudlet that this blueprint is part of."""
#         return self.cloudlet
#
#     def pattern(self):
#         """Returns a pattern object that represents the pattern in the blueprint."""
#         patternString = self.defn['pattern']
#         pattrn = pattern.Pattern(patternString)
#         return pattrn
#
#     def provider_name(self):
#         """returns a provider pbjects that corresponds to the one indicated in the blueprint."""
#         providerString = self.defn['provider']
#
#         return providerString
