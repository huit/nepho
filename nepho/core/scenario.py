# coding: utf-8
import yaml
from nepho.core import common, pattern, resource, config, context, provider, provider_factory
from os import path

class Scenario:
    """A class that encapsulates a blueprint with an actual parameter and config environment."""
    
    def __init__(self, config, bprint, params):

        self.config = config
        self.blueprint = bprint 
        self.transient_params = params
        
        self.resourceManager = resource.ResourceManager(config)
        self.contextManager = context.ContextManager(config)
        self.contextManager.set_blueprint(bprint)
        self.contextManager.add_params(params)
        
        self.provider = None
        self.pattern = None
       
        
    def get_provider(self):
        """Return the relevant provider for this blueprint."""
        if self.provider is None:
            provider_name = self.blueprint.provider_name()
            factory = provider_factory.ProviderFactory()
            self.provider = factory.create(provider_name, self.config, self)
#            self.provider.load_pattern(self.blueprint)
        return self.provider
       
    def get_context(self):
        """Generate a context for this scenario."""
        return self.contextManager.generate()    
    
    def get_template(self):
        """Return a generated template file for this blueprint and these params & configs."""
        
        providr = self.get_provider()
        pattern = self.get_pattern()
        ctx = self.get_context()
        print pattern
        print ctx
        
        template_string = self.resourceManager.render_template(self)
        return providr.format_template(template_string)

    def get_pattern(self):
        """Loads in a blueprint, looks up the pattern, and configures the context."""
        if self.pattern is None:
            providr = self.get_provider()
            pattern_str = self.blueprint.pattern()
            pattern_file = self.resourceManager.lookup_pattern_file(self.blueprint, providr)
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
#     
#             
#         

