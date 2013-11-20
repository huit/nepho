from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Config
class a_TestNephoConfig(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoConfig, self).setUp()

        self.reset_backend()

    def test_nepho_config_list(self):
        app = self.make_app(argv=['config', 'list'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_config_set(self):
        app = self.make_app(argv=['config', 'set', 'test_key', 'test_value'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_config_get(self):
        app = self.make_app(argv=['config', 'get', 'test_key'])
        app.setup()
        app.run()
        app.close()
