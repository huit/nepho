from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


class BasicNephoTests(test.CementTestCase):
    app_class = NephoTestApp

    def test_nepho_default(self):
        self.app.setup()
        self.app.run()
        self.app.close()


# Test Cloudlet
class a_TestNephoCloudlet(test.CementTestCase):
    app_class = NephoTestApp


# Test Blueprint
class TestNephoBlueprint(test.CementTestCase):
    app_class = NephoTestApp


# Test Config
class TestNephoConfig(test.CementTestCase):
    app_class = NephoTestApp

    def test_nepho_config_list(self):
        app = self.make_app(argv=['config', 'list'])
        app.setup()
        app.run()
        app.close()


# Test Parameter
class TestNephoParameter(test.CementTestCase):
    app_class = NephoTestApp


# Test Scope
class TestNephoScope(test.CementTestCase):
    app_class = NephoTestApp


# Test Stack
class TestNephoStack(test.CementTestCase):
    app_class = NephoTestApp
