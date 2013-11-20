from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Parameter
class a_TestNephoParameter(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoParameter, self).setUp()

        self.reset_backend()

        app = self.make_app(argv=['cloudlet', '--quiet', 'uninstall', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['cloudlet', '--quiet', 'install', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['parameter', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_list(self):
        app = self.make_app(argv=['parameter', 'list'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_set(self):
        app = self.make_app(argv=['parameter', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_add(self):
        app = self.make_app(argv=['parameter', 'add', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_get(self):
        app = self.make_app(argv=['parameter', 'get', 'test_key'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_unset(self):
        app = self.make_app(argv=['parameter', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['parameter', 'unset', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_remove(self):
        app = self.make_app(argv=['parameter', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['parameter', 'remove', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_parameter_delete(self):
        app = self.make_app(argv=['parameter', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['parameter', 'delete', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()
