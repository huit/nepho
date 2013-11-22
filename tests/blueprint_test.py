from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Blueprint
class a_TestNephoBlueprint(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoBlueprint, self).setUp()

        self.reset_backend()

        app = self.make_app(argv=['cloudlet', '--quiet', 'uninstall', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['cloudlet', '--quiet', 'install', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_blueprint_list(self):
        app = self.make_app(argv=['blueprint', 'list', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_blueprint_describe(self):
        app = self.make_app(argv=['blueprint', 'describe', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()
