# coding: utf-8
from nepho.providers import vagrant_provider, aws_provider, openstack_provider


class ProviderFactory:
    """A factory that creates provider-specific driver classes"""

    def init(self, name, config, scenario=None):
        # TODO: do something clever here by parsing the "providers" module and contents.

        if name == "vagrant":
            return vagrant_provider.VagrantProvider(config, scenario)
        elif name == "aws":
            return aws_provider.AWSProvider(config, scenario)
        elif name == "openstack":
            return openstack_provider.OpenStackProvider(config, scenario)