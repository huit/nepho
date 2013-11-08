# coding: utf-8

from nepho.core import common, resource, pattern, provider
from os import path


class AnisbleProvider:
    """An infrastructure provider class for ansible"""

    PROVIDER_ID = "ansible"
    TEMPLATE_FILENAME = "playbook.yaml"

    def deploy(self):
        """Deploy a given pattern."""
        pass

    def undeploy(self):
        pass
