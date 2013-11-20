from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Scope
class a_TestNephoScope(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoScope, self).setUp()

        self.reset_backend()

    def test_nepho_scope_default(self):
        app = self.make_app(argv=['scope', 'default', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['scope', 'default'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_scope_set(self):
        app = self.make_app(argv=['scope', 'set', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['scope', 'set'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_scope_unset(self):
        app = self.make_app(argv=['scope', 'default', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['scope', 'unset', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_scope_clear(self):
        app = self.make_app(argv=['scope', 'default', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['scope', 'clear', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
